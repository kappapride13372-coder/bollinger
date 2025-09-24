import pandas as pd
import requests
import numpy as np
from tqdm import tqdm
import backtrader as bt
import multiprocessing as mp
import os
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt
from itertools import product

# ===========================
# Parameters
# ===========================
tickers = ['BBUSDT','BATUSDT','DASHUSDT','NFPUSDT','NEIROUSDT','RESOLVUSDT','SNXUSDT',
           'AGLDUSDT','HAEDALUSDT','LINKUSDT','GMXUSDT','MUBARAKUSDT','KERNELUSDT','ORDIUSDT',
           'ALTUSDT','COWUSDT','RVNUSDT','DUSDT','VICUSDT','BLURUSDT','WLDUSDT','CTKUSDT',
           'ARBUSDT','KNCUSDT','THEUSDT','RAREUSDT','HBARUSDT','IOTAUSDT','PNUTUSDT','ROSEUSDT',
           'ERAUSDT','VANRYUSDT','DOGEUSDT','SPELLUSDT','PARTIUSDT','PERPUSDT','1INCHUSDT',
           'HYPERUSDT','VIRTUALUSDT','ZILUSDT','REZUSDT','SSVUSDT','EGLDUSDT','BABYUSDT','NEWTUSDT',
           'WCTUSDT','MANAUSDT','SXPUSDT','RADUSDT','PEPEUSDT','1000SATSUSDT','ACTUSDT','TRBUSDT',
           'AVAXUSDT','ZKUSDT','ASTRUSDT','BANDUSDT','MAGICUSDT','NEARUSDT','CKBUSDT','NTRNUSDT',
           'RENDERUSDT','TSTUSDT','DOTUSDT','ORCAUSDT','MASKUSDT','PLUMEUSDT','IDUSDT','CHZUSDT','FETUSDT']

interval = "2h"
fixed_trade_size = 1000
STARTING_CASH = 100000
NUM_CORES = 6
CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "ticker_data_cache.pkl")

adr_period_range = [120, 240]
adr_multiplier_range = [1.5, 2, 2.5, 3]
ema_period_range = [30, 60, 90]
stop_loss_range = [1.5, 2, 2.5]

os.makedirs(CACHE_DIR, exist_ok=True)

# ===========================
# Data fetching
# ===========================
def fetch_12000_candles(ticker, interval="4h"):
    url = "https://api.binance.com/api/v3/klines"
    all_data = []
    limit_per_request = 1000
    end_time = None
    for i in range(12):
        params = {"symbol": ticker, "interval": interval, "limit": limit_per_request}
        if end_time:
            params["endTime"] = end_time - 1
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"⚠️ Failed to fetch {ticker}: {e}")
            return None
        if not data:
            break
        all_data.extend(data)
        end_time = data[0][0]
        if len(data) < limit_per_request:
            break
    if not all_data:
        print(f"⚠️ No candle data for {ticker}")
        return None
    all_data.reverse()
    df = pd.DataFrame(all_data, columns=[
        "timestamp","open","high","low","close","volume",
        "close_time","quote_asset_volume","num_trades",
        "taker_base","taker_quote","ignore"
    ])
    df[['open','high','low','close','volume']] = df[['open','high','low','close','volume']].astype(float)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('datetime', inplace=True)
    df = df[['open','high','low','close','volume']]
    df = df[~df.index.duplicated(keep='first')]
    df.sort_index(inplace=True)
    cache_file = os.path.join(CACHE_DIR, f"{ticker}.pkl")
    with open(cache_file, "wb") as f:
        pickle.dump(df, f)
    print(f"✅ {ticker}: fetched {len(df)} candles")
    return df

# ===========================
# Strategy
# ===========================
class ADR_EMA_Stop_Strategy(bt.Strategy):
    params = dict(
        adr_period=120,
        adr_multiplier=1.5,
        ema_period=30,
        stop_loss_multiplier=1.5,
        trade_size=fixed_trade_size
    )

    def __init__(self):
        self.ema = bt.ind.EMA(self.data.close, period=self.p.ema_period)
        self.adr = bt.indicators.AverageTrueRange(period=self.p.adr_period)

        # bookkeeping
        self.entry_bar = None
        self.trade_log = []
        self.entry_price = None
        self.exit_price = None
        self.above_ema_since_entry = False
        self.stop_order = None
        self.entry_order = None
        self._pending_exit_reason = None

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                # entry fill
                self.entry_price = order.executed.price
                self.entry_bar = len(self)
                self.above_ema_since_entry = self.entry_price > self.ema[0]

                # place stop after fill
                adr_value = self.adr[0]
                stop_price = self.entry_price - self.p.stop_loss_multiplier * adr_value
                self.stop_order = self.sell(size=order.executed.size,
                                            exectype=bt.Order.Stop,
                                            price=stop_price)

            elif order.issell():
                # exit fill
                self.exit_price = order.executed.price
                self._record_trade(exit_reason=self._pending_exit_reason or "stop/close")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.entry_order = None

    def next(self):
        if self.data.close[0] <= 0:
            return

        if not self.position:
            # breakout condition
            bar_change = ((self.data.close[0] - self.data.close[-1]) / self.data.close[-1]) * 100
            adr_value = self.adr[0]

            if bar_change >= self.p.adr_multiplier * adr_value:
                size = self.p.trade_size / self.data.close[0]
                self.entry_order = self.buy(size=size, exectype=bt.Order.Market)

        else:
            if self.data.close[0] > self.ema[0]:
                self.above_ema_since_entry = True

            if self.above_ema_since_entry and self.data.close[0] < self.ema[0]:
                self.close_trade(exit_reason="ema_exit")

    def close_trade(self, exit_reason):
        if self.position:
            if self.stop_order:
                self.cancel(self.stop_order)
                self.stop_order = None
            self._pending_exit_reason = exit_reason
            self.close()

    def _record_trade(self, exit_reason):
        if self.entry_price is None or self.exit_price is None:
            return

        duration_bars = len(self) - self.entry_bar if self.entry_bar else None
        pnl = (self.exit_price - self.entry_price) * (self.p.trade_size / self.entry_price)
        pnl_pct = (pnl / self.p.trade_size) * 100

        self.trade_log.append({
            "ticker": self.data._name or "unknown",
            "adr_period": self.p.adr_period,
            "adr_multiplier": self.p.adr_multiplier,
            "ema_period": self.p.ema_period,
            "stop_loss_multiplier": self.p.stop_loss_multiplier,
            "entry_bar": self.entry_bar,
            "exit_bar": len(self),
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "pnl": pnl,
            "pnl_pct": pnl_pct,
            "duration_bars": duration_bars,
            "result": "win" if pnl > 0 else "loss",
            "exit_reason": exit_reason
        })

        # reset
        self.entry_bar = None
        self.entry_price = None
        self.exit_price = None
        self.above_ema_since_entry = False
        self.stop_order = None
        self.entry_order = None
        self._pending_exit_reason = None

# ===========================
# Backtest Worker
# ===========================
def backtest_worker(args):
    ticker, df, adr_period, adr_mult, ema_period, stop_mult = args
    if df is None or df.empty:
        return None
    try:
        cerebro = bt.Cerebro()
        cerebro.addstrategy(ADR_EMA_Stop_Strategy,
                            adr_period=adr_period,
                            adr_multiplier=adr_mult,
                            ema_period=ema_period,
                            stop_loss_multiplier=stop_mult)
        bt_data = bt.feeds.PandasData(dataname=df, open='open', high='high', low='low',
                                      close='close', volume='volume', plot=False, name=ticker)
        cerebro.adddata(bt_data)
        cerebro.broker.setcash(STARTING_CASH)
        cerebro.broker.setcommission(commission=0.001)
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        result = cerebro.run(maxcpus=1)[0]
    except Exception as e:
        print(f"⚠️ Backtest failed for {ticker}: {e}")
        return None

    trades = getattr(result, 'trade_log', [])
    trade_pnls = [t['pnl'] for t in trades]
    total_pnl = sum(trade_pnls)
    total_trades = len(trade_pnls)
    n_wins = sum(1 for pnl in trade_pnls if pnl > 0)
    n_losses = sum(1 for pnl in trade_pnls if pnl <= 0)
    drawdown = result.analyzers.drawdown.get_analysis()
    max_dd = drawdown.get('max', {}).get('drawdown', 0)
    return {
        'ticker': ticker,
        'adr_period': adr_period,
        'adr_multiplier': adr_mult,
        'ema_period': ema_period,
        'stop_loss_multiplier': stop_mult,
        'total_trades': total_trades,
        'n_wins': n_wins,
        'n_losses': n_losses,
        'total_pnl': total_pnl,
        'avg_pnl_per_trade': total_pnl / total_trades if total_trades else 0,
        'max_drawdown': max_dd,
        'trades': trades
    }

# ===========================
# Main
# ===========================
def main():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            ticker_data = pickle.load(f)
    else:
        ticker_data = {}
        for ticker in tqdm(tickers, desc="Fetching tickers"):
            df = fetch_12000_candles(ticker, interval=interval)
            if df is not None and not df.empty:
                ticker_data[ticker] = df
        with open(CACHE_FILE, "wb") as f:
            pickle.dump(ticker_data, f)

    if not ticker_data:
        print("❌ No data fetched.")
        return

    worker_args = []
    for adr_period, adr_mult, ema_period, stop_mult in product(
        adr_period_range, adr_multiplier_range, ema_period_range, stop_loss_range
    ):
        for ticker, df in ticker_data.items():
            worker_args.append((ticker, df, adr_period, adr_mult, ema_period, stop_mult))

    mp.set_start_method('spawn', force=True)
    with mp.Pool(NUM_CORES) as pool:
        results = list(tqdm(pool.imap(backtest_worker, worker_args), total=len(worker_args)))

    results = [r for r in results if r is not None]

    trades_by_params = defaultdict(list)
    for r in results:
        trades = r.pop("trades", [])
        key = (r["adr_period"], r["adr_multiplier"], r["ema_period"], r["stop_loss_multiplier"])
        trades_by_params[key].extend(trades)

    summary_rows = []

    for (adr_period, adr_mult, ema_period, stop_mult), trades in trades_by_params.items():
        df_trades = pd.DataFrame(trades)
        if df_trades.empty:
            continue

        df_trades = df_trades.sort_values("exit_bar").reset_index(drop=True)
        df_trades["cum_pnl"] = df_trades["pnl"].cumsum()

        plt.figure(figsize=(10,6))
        plt.plot(df_trades["cum_pnl"], label="Cumulative PnL")
        plt.title(f"Cumulative PnL (ADR={adr_period}, Mult={adr_mult}, EMA={ema_period}, Stop={stop_mult})")
        plt.xlabel("Trades")
        plt.ylabel("PnL ($)")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.5)
        filename_plot = f"equity_ADR{adr_period}_mult{adr_mult}_EMA{ema_period}_Stop{stop_mult}.png"
        plt.savefig(filename_plot)
        plt.close()
        print(f"📈 Saved cumulative PnL curve to {filename_plot}")

        total_trades = len(df_trades)
        total_pnl = df_trades["pnl"].sum()
        avg_pnl = df_trades["pnl"].mean()
        winners = df_trades[df_trades["pnl"] > 0]
        losers = df_trades[df_trades["pnl"] <= 0]
        avg_win_pct = winners["pnl_pct"].mean() if not winners.empty else 0
        avg_loss_pct = losers["pnl_pct"].mean() if not losers.empty else 0
        avg_duration = df_trades["duration_bars"].mean()
        win_rate = len(winners)/total_trades*100 if total_trades else 0

        summary_rows.append({
            "adr_period": adr_period,
            "adr_multiplier": adr_mult,
            "ema_period": ema_period,
            "stop_loss_multiplier": stop_mult,
            "total_trades": total_trades,
            "win_rate_pct": round(win_rate,2),
            "avg_pnl": avg_pnl,
            "avg_win_pct": avg_win_pct,
            "avg_loss_pct": avg_loss_pct,
            "avg_duration_bars": avg_duration,
            "total_pnl": total_pnl
        })

        filename_csv = f"trades_ADR{adr_period}_mult{adr_mult}_EMA{ema_period}_Stop{stop_mult}.csv"
        df_trades.to_csv(filename_csv, index=False)
        print(f"✅ Saved {total_trades} trades to {filename_csv}")

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv("gridsearch_summary.csv", index=False)
    print(f"✅ Saved grid search summary to gridsearch_summary.csv")

    best_row = summary_df.loc[summary_df["total_pnl"].idxmax()]
    print("🏆 Optimal Parameters Found:")
    print(best_row)

if __name__ == "__main__":
    main()
