from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest

client = CryptoHistoricalDataClient()

request_params = CryptoLatestQuoteRequest(symbol_or_symbols='BTC/USD')

latest_quotes = client.get_crypto_latest_quote(request_params)

print(latest_quotes['BTC/USD'].ask_price)