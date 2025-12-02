import backtrader as bt

class TestStrategy(bt.Strategy):
    params = dict(period=2)  # Reduced to match available data

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.period
        )

    def next(self):
        if not self.position: 
            if self.data.close[0] > self.sma[0]:
                self.buy()
        else:
            if self.data.close[0] < self.sma[0]:
                self.sell()
