import vectorbt as vbt
import pandas as pd
from datetime import datetime, timedelta
import pdb

# TODO: PARAMETRIZE THE NUMBER OF DAYS AND TICKERS
start_date = (datetime.now() - timedelta(days=200)).strftime('%Y-%m-%d')
tickers = ['TSLA', 'AAPL', 'GOOG', 'MSFT', 'AMZN']

for ticker in tickers:
    # Need more days: 50 for slow MA + buffer for crossovers to occur
    try:
        price = vbt.YFData.download(ticker, start=start_date).get('Close')
        fast_ma = vbt.MA.run(price, 10)   # 10-day MA indicator
        slow_ma = vbt.MA.run(price, 50)   # 50-day MA indicator

        # Generate entry and exit signals for golden cross strategy
        entries = fast_ma.ma_crossed_above(slow_ma)  # True where fast MA crosses above slow MA
        exits   = fast_ma.ma_crossed_below(slow_ma)  # True where fast MA crosses below slow MA

        # # Debug: Check if signals are being generated
        # print(f'Number of entry signals: {entries.sum()}')
        # print(f'Number of exit signals: {exits.sum()}')

        # Simulate the strategy with $10,000 initial cash
        crossover_final = vbt.Portfolio.from_signals(price, entries, exits, init_cash=10000)
        crossover_pnl = crossover_final.total_profit()
        # print(f'Total Profit/Loss: ${pnl:.2f}')
        # print(f'Final Value: ${crossover_final.value().iloc[-1]:.2f}')
        # print(f'Number of trades: {crossover_final.orders.count().sum()}')

        # Buy and hold comparison
        # Buy at the start, sell at the end
        buy_hold_entry_exit = pd.Series(False, index=price.index)
        # buy_hold_entries = pd.Series(False, index=price.index)
        buy_hold_entry_exit.iloc[0] = True  # Buy at the start
        #buy_hold_exits = pd.Series(False, index=price.index)
        buy_hold_entry_exit.iloc[-1] = True  # Sell at the end

        buy_hold_final = vbt.Portfolio.from_signals(price, buy_hold_entry_exit, buy_hold_entry_exit, init_cash=10000)

        buy_hold_pnl = buy_hold_final.total_profit()
        #buy_hold_final = buy_hold_crossover_final.value().iloc[-1]
        print(buy_hold_final.value().iloc[-1])
        print(buy_hold_pnl)

        print('\n--- Buy and Hold vs Crossover Comparison ---')
        print(f'Buy & Hold Profit/Loss: ${buy_hold_pnl:.2f}')
        print(f'Crossover Profit/Loss: ${crossover_pnl:.2f}')
        
        print(f'\nStrategy vs Buy & Hold:')
        print(f'  Strategy outperformed by: ${crossover_pnl - buy_hold_pnl:.2f}')
        print(f'  Strategy return: {((crossover_final.value().iloc[-1] / 10000) - 1) * 100:.2f}%')
        print(f'  Buy & Hold return: {((buy_hold_final.value().iloc[-1] / 10000) - 1) * 100:.2f}%')
    except Exception as e:
        print(f'Error processing {ticker}: {e}')