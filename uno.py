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
    '1000WHYUSDT','FLOWUSDT','SNXUSDT','CELOUSDT','ATAUSDT','TAOUSDT','COSUSDT','MORPHOUSDT','PYTHUSDT','TNSRUSDT',
    'B3USDT','KMNOUSDT','BANUSDT','TOKENUSDT','EPICUSDT','NKNUSDT','CKBUSDT','PROMPTUSDT','MOVRUSDT','SEIUSDT',
    'CTSIUSDT','SXTUSDT','BROCCOLIF3BUSDT','YGGUSDT','HOMEUSDT','MINAUSDT','FXSUSDT','TACUSDT','ONEUSDT','BEAMXUSDT',
    'AVAAIUSDT','LPTUSDT','GUSDT','JSTUSDT','TRUMPUSDT','THEUSDT','DMCUSDT','DOODUSDT','MOVEUSDT','RVNUSDT',
    '1INCHUSDT','DOGSUSDT','BIGTIMEUSDT','UMAUSDT','ONTUSDT','DEEPUSDT','AAVEUSDT','HUSDT','BANDUSDT','LUNA2USDT',
    'ZKJUSDT','ARBUSDT','ALTUSDT','MANAUSDT','LAYERUSDT','POWRUSDT','GALAUSDT','VELODROMEUSDT','TUSDT','INJUSDT',
    'DEGOUSDT','PROVEUSDT','HBARUSDT','CYBERUSDT','CFXUSDT','PHAUSDT','SXPUSDT','VTHOUSDT','CVXUSDT','IOTAUSDT',
    'MELANIAUSDT','HOOKUSDT','ZETAUSDT','RLCUSDT','ARCUSDT','PONKEUSDT','1000XECUSDT','TAKEUSDT','USUALUSDT','DYMUSDT',
    'HFTUSDT','API3USDT','STEEMUSDT','NXPCUSDT','ICNTUSDT','ATOMUSDT','GHSTUSDT','AUSDT','QUICKUSDT','ALGOUSDT',
    'POPCATUSDT','FISUSDT','QUSDT','PUFFERUSDT','BICOUSDT','TAGUSDT','B2USDT','FORTHUSDT','VANAUSDT','ARIAUSDT',
    'BANANAS31USDT','TRADOORUSDT','BERAUSDT','AIAUSDT','TURBOUSDT','ALCHUSDT','CGPTUSDT','OBOLUSDT','PUMPBTCUSDT','TRUUSDT',
    'MBOXUSDT','NEOUSDT','BTRUSDT','ERAUSDT','GASUSDT','PUNDIXUSDT','DUSDT','FLOCKUSDT','HOLOUSDT','MUBARAKUSDT',
    'JTOUSDT','STBLUSDT','SOONUSDT','TSTUSDT','WALUSDT','ONGUSDT','DOTUSDT','CATIUSDT','SUNUSDT','BNTUSDT',
    'GRTUSDT','ICPUSDT','XAIUSDT','1000XUSDT','SPELLUSDT','KSMUSDT','QNTUSDT','MERLUSDT','YFIUSDT','RIFUSDT',
    'JOEUSDT','ACHUSDT','NFPUSDT','TAUSDT','FLUIDUSDT','1000000MOGUSDT','CUSDT','MOCAUSDT','1000CATUSDT','ASTERUSDT',
    'ADAUSDT','SLERFUSDT','CVCUSDT','ORDIUSDT','MUSDT','XNYUSDT','SIGNUSDT','VELVETUSDT','PLUMEUSDT','LTCUSDT',
    'VIRTUALUSDT','LDOUSDT','NMRUSDT','ETCUSDT','AVNTUSDT','LINKUSDT','POLUSDT','SANDUSDT','AVAXUSDT','BTCDOMUSDT',
    'SYRUPUSDT','BNBUSDT','PTBUSDT','WAXPUSDT','VINEUSDT','1000PEPEUSDT','TRBUSDT','OPENUSDT','BANANAUSDT','RESOLVUSDT',
    'ZRXUSDT','ENAUSDT','GOATUSDT','SANTOSUSDT','SAFEUSDT','EDUUSDT','ETHFIUSDT','MITOUSDT','SOLVUSDT','HOTUSDT',
    'COOKIEUSDT','FETUSDT','CETUSUSDT','MLNUSDT','ACEUSDT','NEIROETHUSDT','DUSKUSDT','APEUSDT','FIDAUSDT','ACTUSDT',
    'JASMYUSDT','BMTUSDT','SCRTUSDT','XRPUSDT','NEARUSDT','GRIFFAINUSDT','ZEREBROUSDT','ANIMEUSDT','ENSUSDT','TONUSDT',
    'DASHUSDT','AI16ZUSDT','1000SHIBUSDT','SFPUSDT','BCHUSDT','BAKEUSDT','PUMPUSDT','EGLDUSDT','COMPUSDT','PENGUUSDT',
    'BLURUSDT','BIDUSDT','C98USDT','ARKMUSDT','VOXELUSDT','AWEUSDT','MEUSDT','XVGUSDT','1000FLOKIUSDT','QTUMUSDT',
    'GMXUSDT','METISUSDT','ZECUSDT','ZRCUSDT','ORCAUSDT','BSVUSDT','ICXUSDT','NAORISUSDT','ONDOUSDT','ZILUSDT',
    'AKTUSDT','XLMUSDT','COWUSDT','VANRYUSDT','BARDUSDT','IOTXUSDT','SCRUSDT','DRIFTUSDT','FORMUSDT',
    'OPUSDT','WLDUSDT','ARUSDT','LAUSDT','SUIUSDT','CRVUSDT','DAMUSDT','YALAUSDT','BLESSUSDT','KAIAUSDT',
    'WUSDT','DIAUSDT','KDAUSDT','BATUSDT','DENTUSDT','AIXBTUSDT','SOLUSDT','1000BONKUSDT','JUPUSDT','EIGENUSDT',
    'SONICUSDT','APTUSDT','ARKUSDT','NEIROUSDT','VICUSDT','PAXGUSDT','XTZUSDT','SKYUSDT','AIUSDT','PEOPLEUSDT',
    'BTCUSDT','KAITOUSDT','BUSDT','WCTUSDT','VVVUSDT','ETHUSDT','IOUSDT','OGNUSDT','RSRUSDT','MAGICUSDT',
    'IOSTUSDT','SWELLUSDT','LINEAUSDT','FARTCOINUSDT','1000CHEEMSUSDT','GPSUSDT','BOMEUSDT','HUMAUSDT','ZKUSDT','TRXUSDT',
    'RENDERUSDT','LSKUSDT','AXSUSDT','XPLUSDT','SAGAUSDT','KOMAUSDT','REDUSDT','THETAUSDT','RDNTUSDT','BULLAUSDT',
    'CHRUSDT','RONINUSDT','WIFUSDT','COTIUSDT','SQDUSDT','HMSTRUSDT','BDXNUSDT','KNCUSDT','SYSUSDT','SWARMSUSDT',
    'DYDXUSDT','ILVUSDT','AEROUSDT','XMRUSDT','1MBABYDOGEUSDT','USELESSUSDT','FIOUSDT','PIPPINUSDT','SUSDT','GMTUSDT',
    'HEIUSDT','VETUSDT','WLFIUSDT','PORT3USDT','STRKUSDT','FILUSDT','USDCUSDT','PENDLEUSDT','CAKEUSDT','DOGEUSDT',
    'ASTRUSDT','GLMUSDT','MOODENGUSDT','SOPHUSDT','TIAUSDT','BIOSDT','ETHWUSDT','POLYXUSDT','MASKUSDT','IPUSDT',
    'TWTUSDT','DOLOUSDT','USTCUSDT','PNUTUSDT','AEVOUSDT','HEMIUSDT','DEXEUSDT','PROMUSDT','FUNUSDT','RAYSOLUSDT',
    'MYXUSDT','SOMIUSDT','TUTUSDT','NTRNUSDT','BANKUSDT','SAHARAUSDT','UNIUSDT','KASUSDT','BBUSDT','SSVUSDT',
    'AINUSDT','IDUSDT','LQTYUSDT','IMXUSDT','ZROUSDT','HAEDALUSDT','FUSDT','SUSHIUSDT','WOOUSDT','ZKCUSDT',
    'HYPEUSDT','ZORAUSDT','AIOTUSDT','STXUSDT','OGUSDT','AGLDUSDT','1000LUNCUSDT','SUPERUSDT','RAREUSDT','PHBUSDT',
    'JELLYJELLYUSDT','OXTUSDT','0GUSDT','SKATEUSDT','BRETTUSDT','AIOUSDT','TOSHIUSDT','CHZUSDT','OLUSDT','TAIKOUSDT',
    'UBUSDT','SPXUSDT','AERGOUSDT','SIRENUSDT','MAVUSDT','IDOLUSDT','INUSDT','INITUSDT','BROCCOLI714USDT','KAVAUSDT',
    'SKYAIUSDT','AXLUSDT','ATHUSDT','DEGENUSDT','LUMIAUSDT','HYPERUSDT','CUDISUSDT','TREEUSDT','ESPORTSUSDT','PIXELUSDT',
    'PERPUSDT','ALLUSDT','ROSEUSDT','DFUSDT','SKLUSDT','MEMEUSDT','GUNUSDT','BELUSDT','STORJUSDT','HIVEUSDT',
    'XPINUSDT','NEWTUSDT','TOWNSUSDT','ARPAUSDT','ASRUSDT','LRCUSDT','ENJUSDT','A2ZUSDT','MANTAUSDT','FLUXUSDT',
    'RPLUSDT','AUCTIONUSDT','FHEUSDT','CTKUSDT','SLPUSDT','NOTUSDT','SPKUSDT','NILUSDT','REIUSDT','XVSUSDT',
    '1000000BOBUSDT','PARTIUSDT','CARVUSDT','BABYUSDT','ANKRUSDT','CHESSUSDT','MEWUSDT','STOUSDT','1000RATSUSDT','OMUSDT',
    'SHELLUSDT','HIGHUSDT','REZUSDT','RUNEUSDT','ACXUSDT','SYNUSDT','XCNUSDT','TLMUSDT','PORTALUSDT','SAPIENUSDT',
    'BASUSDT','HIFIUSDT','MYROUSDT','CELRUSDT','LISTAUSDT','STGUSDT','UXLINKUSDT','DODOXUSDT','MILKUSDT','KERNELUSDT',
    'ZENUSDT','MTLUSDT','AGTUSDT','BRUSDT','CHILLGUYUSDT','MAVIAUSDT','AVAUSDT','EPTUSDT','1000SATSUSDT','ALPINEUSDT',
    'ALICEUSDT','GTCUSDT','CROSSUSDT','GRASSUSDT','FLMUSDT','TANSSIUSDT','PLAYUSDT','HIPPOUSDT'
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
