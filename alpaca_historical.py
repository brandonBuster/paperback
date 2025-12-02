from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient
import datetime

api_key = 'PKTCCEZJB47PORIMJO4YY6ONDX'
secret_key = '7RTtLTdrGQrq16NKiybE7XZnpxVWbnwDayJ77TwkmcvD'

ticker = 'TSLA'

client = StockHistoricalDataClient(api_key, secret_key)

request_params = StockBarsRequest(
    symbol_or_symbols=[ticker],
    timeframe=TimeFrame.Day,
    start=datetime.datetime(2024, 1, 1),
)

bars = client.get_stock_bars(request_params)
bars_df = bars.df
print(bars_df)

# Save to CSV file
csv_filename = f'{ticker}_bars.csv'
bars_df.to_csv(csv_filename, index=True)
print(f'Data saved to {csv_filename}')
