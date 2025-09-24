import pandas as pd
import numpy as np
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import time
import datetime

# =======================
# Binance API setup
# =======================
api_key = 'U8J05yLTrjPnyyjjK6PqsadNI6XGwEO53h25PyTfIKBkUpHfiLgTrOYMeyO4mRN7'
api_secret = 'zALQdNiCInvTb7OsrbNJR6pnPGHW1ULAuvMoLyo4vW83V4k78ulGeJemXJ62FDSf'
client = Client(api_key, api_secret)  # Binance.com Germany-based account

# =======================
# Strategy Parameters
# =======================
symbols = [''DOLO/USDT', 'BTTC/USDT', 'BIO/USDT', 'LA/USDT', 'RLC/USDT',
    'DIA/USDT', 'QUICK/USDT', 'ZRX/USDT', 'AI/USDT', 'LISTA/USDT',
    'RP/USDT', 'ONE/USDT', 'CETUS/USDT', 'POL/USDT', 'CRV/USDT',
    'PHA/USDT', 'PIXEL/USDT', 'XAI/USDT', 'YGG/USDT', 'PORTAL/USDT',
    'HFT/USDT', 'COOKIE/USDT', 'C98/USDT', 'VOXEL/USDT', 'SAGA/USDT',
    'ALICE/USDT', 'HOOK/USDT', 'ETHFI/USDT', 'LQTY/USDT', 'AEVO/USDT',
    'LDO/USDT', 'MBOX/USDT', 'TLM/USDT', 'COTI/USDT', 'GTC/USDT',
    'MEME/USDT', 'WIF/USDT', 'ENA/USDT', 'CGPT/USDT', 'SLP/USDT',
    'XVG/USDT', 'SCR/USDT', 'CATI/USDT', 'INIT/USDT', 'RAY/USDT',
    'AIXBT/USDT', 'REI/USDT', 'CELR/USDT', 'ARKM/USDT', 'PENGU/USDT',
    'BEAMX/USDT', 'SHELL/USDT', 'IO/USDT', 'EIGEN/USDT', 'STO/USDT',
    'BICO/USDT', 'FLOW/USDT', 'BAKE/USDT', 'DYM/USDT', 'CVX/USDT',
    'VELODROME/USDT', 'MDT/USDT', 'ZRO/USDT', 'IMX/USDT', 'ACA/USDT',
    'FIDA/USDT', 'HIGH/USDT', 'UMA/USDT', 'TRU/USDT', 'ENJ/USDT',
    'BANANA/USDT', 'CTSI/USDT', 'BOME/USDT', 'GALA/USDT', 'SEI/USDT',
    'CHESS/USDT', '1000CAT/USDT', 'PHB/USDT', 'TAO/USDT', 'RUNE/USDT',
    'SUSHI/USDT', 'OMNI/USDT', 'USUAL/USDT', 'JASMY/USDT', 'TIA/USDT',
    'SPK/USDT', 'CHR/USDT', 'GUN/USDT', 'ICP/USDT', 'MANTA/USDT',
    'ILV/USDT', 'SOPH/USDT', 'GPS/USDT', 'DOGS/USDT', 'KDA/USDT',
    'OSMO/USDT', 'RSR/USDT', 'PYR/USDT', 'BMT/USDT', 'METIS/USDT',
    'BB/USDT', 'BAT/USDT', 'DASH/USDT', 'NFP/USDT', 'NEIRO/USDT',
    'RESOLV/USDT', 'SNX/USDT', 'AGLD/USDT', 'HAEDAL/USDT', 'LINK/USDT',
    'GMX/USDT', 'MUBARAK/USDT', 'KERNEL/USDT', 'ORDI/USDT', 'ALT/USDT',
    'COW/USDT', 'RVN/USDT', 'D/USDT', 'VIC/USDT', 'BLUR/USDT',
    'WLD/USDT', 'CTK/USDT', 'ARB/USDT', 'KNC/USDT', 'THE/USDT',
    'RARE/USDT', 'HBAR/USDT', 'IOTA/USDT', 'PNUT/USDT', 'ROSE/USDT',
    'ERA/USDT', 'VANRY/USDT', 'DOGE/USDT', 'SPELL/USDT', 'PARTI/USDT',
    'PERP/USDT', '1INCH/USDT', 'HYPER/USDT', 'VIRTUAL/USDT', 'ZIL/USDT',
    'REZ/USDT', 'SSV/USDT', 'EGLD/USDT', 'BABY/USDT', 'NEWT/USDT',
    'WCT/USDT', 'MANA/USDT', 'SXP/USDT', 'RAD/USDT', 'PEPE/USDT',
    '1000SATS/USDT', 'ACT/USDT', 'TRB/USDT', 'AVAX/USDT', 'ZK/USDT',
    'ASTR/USDT', 'BAND/USDT', 'MAGIC/USDT', 'NEAR/USDT', 'CKB/USDT',
    'NTRN/USDT', 'RENDER/USDT', 'TST/USDT', 'DOT/USDT', 'ORCA/USDT',
    'MASK/USDT', 'PLUME/USDT', 'ID/USDT', 'CHZ/USDT', 'FET/USDT',
    'HUMA/USDT', 'LUMIA/USDT', 'ANIME/USDT', 'SYN/USDT', 'CELO/USDT',
    'SOL/USDT', 'STX/USDT', 'LRC/USDT', 'HOT/USDT', 'TURBO/USDT',
    'AXL/USDT', 'STRK/USDT', 'OGN/USDT', 'INJ/USDT', 'MINA/USDT',
    'LPT/USDT', 'TOWNS/USDT', 'BNSOL/USDT', 'FIL/USDT', 'ADA/USDT',
    'ETC/USDT', 'STG/USDT', 'FIO/USDT', 'MBL/USDT', 'FLOKI/USDT',
    'VTHO/USDT', 'MOVR/USDT', '1MBABYDOGE/USDT', 'OP/USDT', 'PEOPLE/USDT',
    'CYBER/USDT', 'GRT/USDT', 'ADX/USDT', 'YFI/USDT', 'A2Z/USDT',
    'WBETH/USDT', 'LUNA/USDT', 'XLM/USDT', 'IOTX/USDT', 'JUP/USDT',
    'ARPA/USDT', 'S/USDT', 'ALGO/USDT', 'FXS/USDT', 'UNI/USDT',
    'OM/USDT', 'ATOM/USDT', 'ZEN/USDT', 'JTO/USDT', 'PENDLE/USDT',
    'CFX/USDT', 'SXT/USDT', 'SHIB/USDT', 'ETH/USDT', 'VANA/USDT',
    'TRUMP/USDT', 'MITO/USDT', 'LUNC/USDT', 'DYDX/USDT', 'ANKR/USDT',
    'AR/USDT', 'SYRUP/USDT', 'SUI/USDT', 'APT/USDT', 'TUT/USDT',
    'BIGTIME/USDT', 'GAS/USDT', 'LAYER/USDT', 'ONDO/USDT', 'BROCCOLI714/USDT',
    'SAND/USDT', 'ENS/USDT', 'ONT/USDT', 'NOT/USDT', 'API3/USDT',
    'OXT/USDT', 'GMT/USDT', 'SUPER/USDT', 'W/USDT', 'AUCTION/USDT',
    'ACH/USDT', 'A/USDT', 'BAR/USDT', 'CAKE/USDT', 'KAITO/USDT',
    'XTZ/USDT', 'KAIA/USDT', 'TNSR/USDT', 'APE/USDT', 'BONK/USDT',
    'VET/USDT', 'ONG/USDT', 'NEO/USDT', 'XRP/USDT', 'AAVE/USDT',
    'IOST/USDT', 'AUDIO/USDT', 'THETA/USDT', 'LTC/USDT', 'QNT/USDT',
    'SOLV/USDT', 'RONIN/USDT', 'ASR/USDT', 'ACE/USDT', 'EPIC/USDT',
    'MOVE/USDT', 'TREE/USDT', 'NXPC/USDT', 'USTC/USDT', 'COMP/USDT',
    'BNB/USDT', 'JST/USDT', 'AMP/USDT', 'KAVA/USDT', 'JUV/USDT',
    'HEI/USDT', 'DEGO/USDT', 'CITY/USDT', 'SLF/USDT', 'SIGN/USDT',
    'KSM/USDT', 'TKO/USDT', 'SAHARA/USDT', 'BTC/USDT', 'WBTC/USDT',
    'TON/USDT', 'QTUM/USDT', 'KMNO/USDT', 'PROVE/USDT', 'SUN/USDT',
    'TRX/USDT', 'SANTOS/USDT', 'PROM/USDT', 'BERA/USDT', 'PAXG/USDT',
    '1000CHEEMS/USDT', 'NEXO/USDT', 'FUN/USDT', 'SKL/USDT', 'OG/USDT',
    'EUR/USDT', 'ZEC/USDT', 'EURI/USDT', 'FDUSD/USDT', 'XUSD/USDT',
    'USD1/USDT', 'USDC/USDT', 'BFUSD/USDT', 'NMR/USDT', 'MKR/USDT',
    'BANANAS31/USDT', 'BCH/USDT', 'HOME/USDT', 'RED/USDT', 'PYTH/USDT',
    'ACM/USDT', 'AXS/USDT', 'C/USDT', 'HIFI/USDT', 'ALPINE/USDT',
    'FORM/USDT', 'FIS/USDT', 'JOE/USDT', 'MAV/USDT', 'IDEX/USDT'
]]  # list of tickers
interval = Client.KLINE_INTERVAL_4HOUR
bollinger_length = 180
bollinger_std = 3
equity = 10000  # starting equity in USDT
position_size_pct = 0.10
stop_loss_pct = 0.40

# =======================
# Helper Functions
# =======================
def fetch_klines(symbol, interval, limit=1000):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def calculate_bollinger(df):
    df['mean'] = df['close'].rolling(bollinger_length).mean()
    df['std'] = df['close'].rolling(bollinger_length).std()
    df['upper'] = df['mean'] + bollinger_std * df['std']
    df['lower'] = df['mean'] - bollinger_std * df['std']
    return df

def get_current_price(symbol):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        print(f"Error fetching live price for {symbol}: {e}")
        return None

def time_until_next_candle(df):
    """Returns seconds until next 4H candle close"""
    last_close_time = df['timestamp'].iloc[-1]
    next_close_time = last_close_time + pd.Timedelta(hours=4)
    return max((next_close_time - datetime.datetime.utcnow()).total_seconds(), 0)

# =======================
# Portfolio & Positions
# =======================
positions = {s: [] for s in symbols}
trades = {s: [] for s in symbols}

# =======================
# Function to scan for new entry
# =======================
def scan_for_entry(symbol, df):
    last_candle = df.iloc[-1]
    if len(positions[symbol]) == 0 and last_candle['close'] < last_candle['lower']:
        qty = (equity * position_size_pct) / last_candle['close']
        position = {
            'entry_price': last_candle['close'],
            'qty': qty,
            'time': datetime.datetime.utcnow(),
            'stop_loss': last_candle['close'] * (1 - stop_loss_pct)
        }
        positions[symbol].append(position)
        print(f"[{symbol}] New position entered at {last_candle['close']:.2f} USDT")

# =======================
# Main Loop
# =======================
while True:
    try:
        # Fetch candles once per loop (assume same for all symbols)
        df_main = fetch_klines(symbols[0], interval, limit=1000)
        df_main = calculate_bollinger(df_main)

        # Countdown until next 4H candle close
        seconds_to_next = time_until_next_candle(df_main)
        minutes, seconds = divmod(int(seconds_to_next), 60)

        # Loop through all symbols
        for symbol in symbols:
            df = fetch_klines(symbol, interval, limit=1000)
            df = calculate_bollinger(df)

            # Immediate entry scan
            scan_for_entry(symbol, df)

            # Live price for stop-loss
            current_price = get_current_price(symbol)
            for pos in positions[symbol][:]:
                if current_price is None:
                    continue

                # Stop-loss triggers immediately
                if current_price < pos['stop_loss']:
                    loss = (current_price - pos['entry_price']) * pos['qty']
                    trades[symbol].append({
                        'type': 'stop_loss',
                        'entry': pos['entry_price'],
                        'exit': current_price,
                        'profit': loss,
                        'entry_time': pos['time'],
                        'exit_time': datetime.datetime.utcnow(),
                        'duration': (datetime.datetime.utcnow() - pos['time']).total_seconds() / 3600
                    })
                    equity += loss
                    positions[symbol].remove(pos)
                    continue

                # Take-profit on candle close above mean
                last_candle = df.iloc[-1]
                if last_candle['close'] > last_candle['mean']:
                    profit = (last_candle['close'] - pos['entry_price']) * pos['qty']
                    trades[symbol].append({
                        'type': 'take_profit',
                        'entry': pos['entry_price'],
                        'exit': last_candle['close'],
                        'profit': profit,
                        'entry_time': pos['time'],
                        'exit_time': datetime.datetime.utcnow(),
                        'duration': (datetime.datetime.utcnow() - pos['time']).total_seconds() / 3600
                    })
                    equity += profit
                    positions[symbol].remove(pos)

        # Portfolio print
        print(f"Time: {datetime.datetime.utcnow()}")
        print(f"Equity: {equity:.2f} USDT")
        print(f"Time until next entry scan: {minutes}m {seconds}s")
        for symbol in symbols:
            print(f"=== {symbol} ===")
            print(f"Open Positions: {len(positions[symbol])}")
            current_price = get_current_price(symbol)
            for pos in positions[symbol]:
                unrealized = (current_price - pos['entry_price']) * pos['qty'] if current_price else 0
                percent_equity = (pos['qty'] * (current_price if current_price else pos['entry_price'])) / equity * 100
                duration = (datetime.datetime.utcnow() - pos['time']).total_seconds() / 3600
                print(f"Entry: {pos['entry_price']:.2f}, Unrealized PnL: {unrealized:.2f}, %Equity: {percent_equity:.2f}, Duration(h): {duration:.2f}")
            print(f"Closed Trades: {len(trades[symbol])}")
        print("-"*50)

        time.sleep(300)  # wait 5 minutes

    except BinanceAPIException as e:
        print(f"Binance API Error: {e}")
        time.sleep(60)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
