import vectorbt as vbt
import pandas as pd
from datetime import datetime, timedelta
ticker = 'TSLA'

# Need more days: 50 for slow MA + buffer for crossovers to occur
start_date = (datetime.now() - timedelta(days=200)).strftime('%Y-%m-%d')

price = vbt.YFData.download(ticker, start=start_date).get('Close')
fast_ma = vbt.MA.run(price, 10)   # 10-day MA indicator
slow_ma = vbt.MA.run(price, 50)   # 50-day MA indicator

# Generate entry and exit signals for golden cross strategy
entries = fast_ma.ma_crossed_above(slow_ma)  # True where fast MA crosses above slow MA
exits   = fast_ma.ma_crossed_below(slow_ma)  # True where fast MA crosses below slow MA

# Debug: Check if signals are being generated
print(f'Number of entry signals: {entries.sum()}')
print(f'Number of exit signals: {exits.sum()}')

# Simulate the strategy with $100 initial cash
pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=10000)

pnl = pf.total_profit()
print(f'Total Profit/Loss: ${pnl:.2f}')
print(f'Final Value: ${pf.value().iloc[-1]:.2f}')
print(f'Number of trades: {pf.orders.count().sum()}')

# Buy and hold comparison
# Buy at the start, sell at the end
buy_hold_entries = pd.Series(False, index=price.index)
buy_hold_entries.iloc[0] = True  # Buy at the start
buy_hold_exits = pd.Series(False, index=price.index)
buy_hold_exits.iloc[-1] = True  # Sell at the end

buy_hold_pf = vbt.Portfolio.from_signals(price, buy_hold_entries, buy_hold_exits, init_cash=10000)
buy_hold_pnl = buy_hold_pf.total_profit()
buy_hold_final = buy_hold_pf.value().iloc[-1]

print('\n--- Buy and Hold Comparison ---')
print(f'Buy & Hold Profit/Loss: ${buy_hold_pnl:.2f}')
print(f'Buy & Hold Final Value: ${buy_hold_final:.2f}')
print(f'\nStrategy vs Buy & Hold:')
print(f'  Strategy outperformed by: ${pnl - buy_hold_pnl:.2f}')
print(f'  Strategy return: {((pf.value().iloc[-1] / 10000) - 1) * 100:.2f}%')
print(f'  Buy & Hold return: {((buy_hold_final / 10000) - 1) * 100:.2f}%')