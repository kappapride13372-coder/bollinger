import pandas as pd
import numpy as np
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import time
from datetime import datetime, timezone
from colorama import Fore, Style, init

# =======================
# Setup
# =======================
init(autoreset=True)  # auto reset colors after each print

api_key = "U8J05yLTrjPnyyjjK6PqsadNI6XGwEO53h25PyTfIKBkUpHfiLgTrOYMeyO4mRN7"
api_secret = "zALQdNiCInvTb7OsrbNJR6pnPGHW1ULAuvMoLyo4vW83V4k78ulGeJemXJ62FDSf"
client = Client(api_key, api_secret, requests_params={'timeout': 10})  # 10s timeout

# =======================
# Strategy Parameters
# =======================
symbols = [
    "BROCCOLI714USDT","DYMUSDT","MAVUSDT","RAREUSDT","SHELLUSDT","SNXUSDT","AGLDUSDT","TRUUSDT",
    "A2ZUSDT","LUMIAUSDT","MBOXUSDT","SOLUSDT","DIAUSDT","ONEUSDT","THEUSDT","AIUSDT","NFPUSDT",
    "HMSTRUSDT","BBUSDT","ACTUSDT","HOOKUSDT","SXTUSDT","FLOWUSDT","MUBARAKUSDT","DEXEUSDT",
    "1000CATUSDT","THETAUSDT","COOKIEUSDT","AVAXUSDT","LQTYUSDT","EPICUSDT","ACXUSDT","CTSIUSDT",
    "GMTUSDT","QNTUSDT","ARKUSDT","ONGUSDT","WIFUSDT","CYBERUSDT","PORTALUSDT","FIDAUSDT",
    "PIXELUSDT","NEXOUSDT","FORMUSDT","CUSDT","BANANAUSDT","KNCUSDT","LRCUSDT","JASMYUSDT",
    "XAIUSDT","EGLDUSDT","TOWNSUSDT","ILVUSDT","DODOUSDT","QIUSDT","HOLOUSDT","EDUUSDT",
    "VELODROMEUSDT","INITUSDT","MANTAUSDT","BICOUSDT","OPENUSDT","BEAMXUSDT","C98USDT","RDNTUSDT",
    "OXTUSDT","ACEUSDT","PHAUSDT","SKLUSDT","AIXBTUSDT","HYPERUSDT","KAIAUSDT","DOTUSDT","FTTUSDT",
    "ZECUSDT","BONKUSDT","NEARUSDT","PYTHUSDT","PHBUSDT","TNSRUSDT","SFPUSDT","AXLUSDT","AEVOUSDT",
    "YGGUSDT","CELOUSDT","XRPUSDT","ALGOUSDT","XTZUSDT","ZILUSDT","RPLUSDT","ARPAUSDT","JTOUSDT",
    "CKBUSDT","ARKMUSDT","USUALUSDT","QTUMUSDT","ZKUSDT","USTCUSDT","GPSUSDT","BTTCUSDT","SPKUSDT",
    "TAOUSDT","WOOUSDT","GMXUSDT","EIGENUSDT","SIGNUSDT","DGBUSDT","TWTUSDT","CETUSUSDT","MINAUSDT",
    "OMNIUSDT","CGPTUSDT","GUNUSDT","MEMEUSDT","HAEDALUSDT","PEPEUSDT","PARTIUSDT","PUMPUSDT",
    "NILUSDT","SCRTUSDT","NMRUSDT","PROVEUSDT","VETUSDT","WCTUSDT","ASTRUSDT","RESOLVUSDT","ALTUSDT",
    "MOVEUSDT","MAGICUSDT","FETUSDT","RVNUSDT","ARUSDT","1INCHUSDT","ZRXUSDT","ACHUSDT","RENDERUSDT",
    "BIGTIMEUSDT","MASKUSDT","ARBUSDT","UMAUSDT","PUNDIXUSDT","INJUSDT","POLYXUSDT","XVSUSDT","RADUSDT",
    "KAITOUSDT","REDUSDT","ROSEUSDT","HOMEUSDT","XVGUSDT","BANDUSDT","DENTUSDT","APEUSDT","BMTUSDT",
    "ANKRUSDT","ATOMUSDT","SOMIUSDT","CAKEUSDT","VICUSDT","ENSUSDT","KDAUSDT","AUSDT","KSMUSDT",
    "SAGAUSDT","TIAUSDT","AXSUSDT","NEWTUSDT","FILUSDT","ENAUSDT","COSUSDT","HEIUSDT","GLMUSDT",
    "SKYUSDT","DOGEUSDT","BNSOLUSDT","GALAUSDT","HBARUSDT","TRUMPUSDT","VIRTUALUSDT","TUSDT","SSVUSDT",
    "HFTUSDT","PENDLEUSDT","FXSUSDT","ALICEUSDT","1MBABYDOGEUSDT","API3USDT","NOTUSDT","SXPUSDT",
    "PENGUUSDT","GRTUSDT","SUSDT","SUSHIUSDT","IOTAUSDT","BOMEUSDT","TUTUSDT","BLURUSDT","FLOKIUSDT",
    "OMUSDT","SUIUSDT","1000SATSUSDT","TURBOUSDT","LAYERUSDT","AVAUSDT","XECUSDT","SCUSDT","RAYUSDT",
    "STOUSDT","COWUSDT","NEIROUSDT","MANAUSDT","SOPHUSDT","ERAUSDT","UNIUSDT","CHZUSDT","ORCAUSDT",
    "YFIUSDT","COMPUSDT","WUSDT","TRBUSDT","RLCUSDT","PNUTUSDT","LINKUSDT","BNBUSDT","LDOUSDT","POLUSDT",
    "MOVRUSDT","CHESSUSDT","OPUSDT","COTIUSDT","TSTUSDT","ADAUSDT","JUPUSDT","1000CHEEMSUSDT","BELUSDT",
    "NEOUSDT","AWEUSDT","SHIBUSDT","DOGSUSDT","NXPCUSDT","DEGOUSDT","WLDUSDT","METISUSDT","SAHARAUSDT",
    "SANDUSDT","BCHUSDT","AAVEUSDT","TONUSDT","BABYUSDT","BIOUSDT","APTUSDT","SUNUSDT","CFXUSDT","BATUSDT",
    "ANIMEUSDT","IDUSDT","LPTUSDT","ETHFIUSDT","JSTUSDT","ORDIUSDT","PEOPLEUSDT","CRVUSDT","LTCUSDT",
    "JOEUSDT","LUNCUSDT","ETCUSDT","XLMUSDT","WLFIUSDT","DASHUSDT","ETHUSDT","WBETHUSDT","ONDOUSDT",
    "KMNOUSDT","BTCUSDT","PERPUSDT","TREEUSDT","LINEAUSDT","SEIUSDT","KAVAUSDT","PAXGUSDT","PLUMEUSDT",
    "EURUSDT","WBTCUSDT","DYDXUSDT","RUNEUSDT","IOUSDT","STRKUSDT","ENJUSDT","STGUSDT","SUPERUSDT",
    "HOTUSDT","TKOUSDT","AUCTIONUSDT","RONINUSDT","STXUSDT","RIFUSDT","BFUSDUSDT","USD1USDT","USDCUSDT",
    "ICPUSDT","PYRUSDT","CHRUSDT","DOLOUSDT","FDUSDUSDT","GLMRUSDT","ASRUSDT","VTHOUSDT","SCRUSDT",
    "SOLVUSDT","VANRYUSDT","FISUSDT","REZUSDT","MEUSDT","KERNELUSDT","LISTAUSDT","LUNAUSDT","GTCUSDT",
    "USDEUSDT","RSRUSDT","XUSDUSDT","EURIUSDT","TRXUSDT","CVXUSDT","ZKCUSDT","VANAUSDT","ALPINEUSDT",
    "SYRUPUSDT","MBLUSDT","FUNUSDT","0GUSDT","SPELLUSDT","PROMUSDT","CTKUSDT","ZROUSDT","JUVUSDT",
    "FLUXUSDT","BARDUSDT","BERAUSDT","BANANAS31USDT","HUMAUSDT","MITOUSDT","LAUSDT","AVNTUSDT","OGUSDT",
    "IMXUSDT","NKNUSDT","HEMIUSDT","ZENUSDT"
]
interval = Client.KLINE_INTERVAL_4HOUR
bollinger_length = 180
bollinger_std = 3
equity = 10000  # starting equity in USDT
position_size_pct = 0.10
stop_loss_pct = 0.40

# =======================
# Helper Functions
# =======================
def fetch_klines(symbol, interval, limit=1000, retries=5, delay=5):
    for attempt in range(retries):
        try:
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
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
            return df
        except Exception as e:
            print(Fore.RED + f"Error fetching {symbol} klines (attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)
    return None

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
        print(Fore.RED + f"Error fetching live price for {symbol}: {e}")
        return None

# =======================
# Portfolio & Positions
# =======================
positions = {s: [] for s in symbols}
trades = {s: [] for s in symbols}
last_scanned = {s: None for s in symbols}

# =======================
# Trade log file
# =======================
trade_log_file = "trades_log.txt"

def log_trade(trade):
    with open(trade_log_file, "a") as f:
        f.write(
            f"{trade['type'].upper()} | Symbol: {trade['symbol']} | Entry: {trade['entry']:.4f} | Exit: {trade['exit']:.4f} | Profit: {trade['profit']:.4f} | EntryTime: {trade['entry_time']} | ExitTime: {trade['exit_time']} | Duration(h): {trade['duration']:.2f}\n"
        )

# =======================
# Function to scan for entry
# =======================
def scan_for_entry(symbol, last_closed_candle):
    if len(positions[symbol]) == 0 and last_closed_candle['close'] < last_closed_candle['lower']:
        qty = (equity * position_size_pct) / last_closed_candle['close']
        position = {
            'entry_price': last_closed_candle['close'],
            'qty': qty,
            'time': datetime.now(timezone.utc),
            'stop_loss': last_closed_candle['close'] * (1 - stop_loss_pct)
        }
        positions[symbol].append(position)
        print(Fore.GREEN + f"[{symbol}] 🚀 New position entered at {last_closed_candle['close']:.4f} USDT | Qty: {qty:.4f}")

# =======================
# Main Loop
# =======================
try:
    while True:
        for symbol in symbols:
            df = fetch_klines(symbol, interval, limit=1000)
            if df is None or len(df) < bollinger_length:
                continue
            df = calculate_bollinger(df)

            last_closed_candle = df.iloc[-2]
            if last_scanned[symbol] == last_closed_candle['timestamp']:
                continue
            last_scanned[symbol] = last_closed_candle['timestamp']

            # Show scanning status
            print(Fore.CYAN + f"[{symbol}] 🔎 Scanning {last_closed_candle['timestamp']} | Close={last_closed_candle['close']:.4f}, Lower={last_closed_candle['lower']:.4f}")

            current_price = get_current_price(symbol)
            if current_price is None:
                continue

            scan_for_entry(symbol, last_closed_candle)

            for pos in positions[symbol][:]:
                if current_price < pos['stop_loss']:
                    loss = (current_price - pos['entry_price']) * pos['qty']
                    trade = {
                        'symbol': symbol,
                        'type': 'stop_loss',
                        'entry': pos['entry_price'],
                        'exit': current_price,
                        'profit': loss,
                        'entry_time': pos['time'],
                        'exit_time': datetime.now(timezone.utc),
                        'duration': (datetime.now(timezone.utc) - pos['time']).total_seconds() / 3600
                    }
                    trades[symbol].append(trade)
                    log_trade(trade)
                    equity += loss
                    positions[symbol].remove(pos)
                    print(Fore.RED + f"[{symbol}] ❌ Stop loss hit at {current_price:.4f} | PnL: {loss:.2f}")

                elif last_closed_candle['close'] > last_closed_candle['mean']:
                    profit = (last_closed_candle['close'] - pos['entry_price']) * pos['qty']
                    trade = {
                        'symbol': symbol,
                        'type': 'take_profit',
                        'entry': pos['entry_price'],
                        'exit': last_closed_candle['close'],
                        'profit': profit,
                        'entry_time': pos['time'],
                        'exit_time': datetime.now(timezone.utc),
                        'duration': (datetime.now(timezone.utc) - pos['time']).total_seconds() / 3600
                    }
                    trades[symbol].append(trade)
                    log_trade(trade)
                    equity += profit
                    positions[symbol].remove(pos)
                    print(Fore.YELLOW + f"[{symbol}] ✅ Take Profit at {last_closed_candle['close']:.4f} | PnL: {profit:.2f}")

        # --- Portfolio Summary ---
        print(Style.BRIGHT + Fore.MAGENTA + f"\n📊 Portfolio Update @ {datetime.now(timezone.utc)}")
        print(Style.BRIGHT + Fore.GREEN + f"Equity: {equity:.2f} USDT")

        total_realized = sum(trade['profit'] for syms in trades.values() for trade in syms)
        print(Style.BRIGHT + Fore.YELLOW + f"Realized PnL: {total_realized:.2f} USDT")

        total_unrealized = 0
        open_positions_exist = False

        for sym in symbols:
            current_price = get_current_price(sym)
            if current_price is None:
                continue

            for pos in positions[sym]:
                open_positions_exist = True
                unrealized = (current_price - pos['entry_price']) * pos['qty']
                total_unrealized += unrealized
                print(
                    Fore.LIGHTWHITE_EX
                    + f"  [{sym}] Entry: {pos['entry_price']:.4f} | Qty: {pos['qty']:.4f} | "
                      f"Current: {current_price:.4f} | PnL: {unrealized:.2f} USDT"
                )

        print(Style.BRIGHT + Fore.CYAN + f"Unrealized PnL (total): {total_unrealized:.2f} USDT")

        if not open_positions_exist:
            print(Fore.LIGHTBLACK_EX + "No open positions.")

        print(Fore.MAGENTA + "-"*60)
        time.sleep(60)

except KeyboardInterrupt:
    print(Fore.RED + "🛑 Bot stopped manually.")
