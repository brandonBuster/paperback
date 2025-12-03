import vectorbt as vbt
import pandas as pd

#ticker = 'TSLA'
tickers = ['TSLA', 'AAPL', 'GOOG', 'MSFT', 'AMZN']

for ticker in tickers:
    try:
        # Get candlestick data (15m interval - note: 15m data only available for last 60 days)
        # Valid intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 4h, 1d, 5d, 1wk, 1mo, 3mo
        data = vbt.YFData.download(ticker, period='60d', interval='1h').get('Close')

        price = data.dropna()

        bbands = vbt.BBANDS.run(price, window=20, alpha=2)

        lower = bbands.lower
        mid = bbands.middle
        upper = bbands.upper


        entries = price < lower
        exits = price > mid

        pf = vbt.Portfolio.from_signals(
            price, 
            entries, 
            exits, 
            init_cash=10000,
            fees=0.0005,      # 0.05% per trade
            slippage=0.0005,  # 0.05% slippage
            direction='longonly')

        print(f'{ticker} stats:')
        print(pf.stats())
        
    except Exception as e:
        print(f'Error processing {ticker}: {e}')