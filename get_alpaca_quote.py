from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

api_endpoint = 'https://paper-api.alpaca.markets/v2'

api_key = 'PKTCCEZJB47PORIMJO4YY6ONDX'
secret_key = '7RTtLTdrGQrq16NKiybE7XZnpxVWbnwDayJ77TwkmcvD'

ticker = 'TSLA'

client = StockHistoricalDataClient(api_key, secret_key)
multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=ticker)
latest_multisymbol_quotes = client.get_stock_latest_quote(multisymbol_request_params)
# latest_ask_price = latest_multisymbol_quotes.latest_quote.ask_price

#print(latest_multisymbol_quotes)
print(latest_multisymbol_quotes[ticker].ask_price)