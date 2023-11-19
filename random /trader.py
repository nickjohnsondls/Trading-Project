import backtrader
import datetime
from strategies import TestStrategy

cerebro = backtrader.Cerebro()


cerebro.broker.set_cash(1000000)

data = backtrader.feeds.YahooFinanceCSVData(
        dataname='oracle.csv',
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

cerebro.adddata(data)

cerebro.addstrategy(TestStrategy)

print('Starting Portfoliio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())



