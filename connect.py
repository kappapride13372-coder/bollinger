from binance.client import Client

api_key = "U8J05yLTrjPnyyjjK6PqsadNI6XGwEO53h25PyTfIKBkUpHfiLgTrOYMeyO4mRN7"
api_secret = "zALQdNiCInvTb7OsrbNJR6pnPGHW1ULAuvMoLyo4vW83V4k78ulGeJemXJ62FDSf"

client = Client(api_key, api_secret)
print(client.get_account())  # should return account info if IP is whitelisted
