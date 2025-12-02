import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend (saves plots to files)

import backtrader as bt
import pandas as pd
from strategy import TestStrategy


# Read data
data = pd.read_csv('data.csv', parse_dates=['Date'], index_col='Date')

# Create cerebro engine
cerebro = bt.Cerebro()

# Add strategy
cerebro.addstrategy(TestStrategy)

# Add data feed
datafeed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(datafeed)

# Set initial cash
cerebro.broker.setcash(10000.0)

# Add analyzer
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

# Run backtest
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
results = cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Print results
strat = results[0]
print('Sharpe Ratio:', strat.analyzers.sharpe.get_analysis())
print('Returns:', strat.analyzers.returns.get_analysis())

# Plot results and save to file
import os
os.makedirs('/app/output', exist_ok=True)

figs = cerebro.plot(style='candlestick')
if figs:
    output_path = '/app/output/backtest_plot.png'
    figs[0][0].savefig(output_path, dpi=100, bbox_inches='tight')
    print(f'Plot saved to {output_path}')

