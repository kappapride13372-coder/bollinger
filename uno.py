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
    "SANDUSDT","BCHUSDT","AAVEUSDT","TONUSDT","BABYUSDT","BIOSDT","APTUSDT","SUNUSDT","CFXUSDT","BATUSDT",
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
