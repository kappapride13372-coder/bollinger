from binance.client import Client

api_key = "U8J05yLTrjPnyyjjK6PqsadNI6XGwEO53h25PyTfIKBkUpHfiLgTrOYMeyO4mRN7"
api_secret = "zALQdNiCInvTb7OsrbNJR6pnPGHW1ULAuvMoLyo4vW83V4k78ulGeJemXJ62FDSf"

# Connect to Binance.US by specifying the testnet=False and using the US URL
client = Client(api_key, api_secret)

# Simple account check
try:
    account_info = client.get_account()
    print("Connected to Binance.US!")
    print(account_info)
except Exception as e:
    print("Connection failed:", e)
