import requests

url = "https://api.binance.com/api/v3/klines"
params = {"symbol": "BTCUSDT", "interval": "1h", "limit": 5}

try:
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    print("Success! Fetched data:", data)
except Exception as e:
    print("Failed:", e)
