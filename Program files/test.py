import yfinance as yf
from pyalgotrade import strategy
from pyalgotrade.technical import bollinger
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.bar import Frequency
import datetime as dt
from pyalgotrade.dataseries import SequenceDataSeries
import pyalgotrade.plotter as plotter

class PairsTradingStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrumentA, instrumentB, window_size, num_std_dev):
        super(PairsTradingStrategy, self).__init__(feed)
        self.__window_size = window_size
        self.__instrumentA = instrumentA
        self.__instrumentB = instrumentB
        self.__pricesA = feed[instrumentA].getCloseDataSeries()
        self.__pricesB = feed[instrumentB].getCloseDataSeries()
        self.__spread = SequenceDataSeries()
        self.__bbands = bollinger.BollingerBands(self.__spread, window_size, num_std_dev)
        self.__positionA = None
        self.__positionB = None


    def onBars(self, bars):
        if len(self.__pricesA) < self.__window_size or len(self.__pricesB) < self.__window_size:
            return

        # Calculate the current spread
        spread = self.__pricesA[-1] - self.__pricesB[-1]
        self.__spread.append(spread)

        # Make sure Bollinger Bands have been calculated for the current bar
        if not self.__bbands.getLowerBand() or not self.__bbands.getUpperBand() or not self.__bbands.getMiddleBand():
            return

        lower_band = self.__bbands.getLowerBand()[-1]
        upper_band = self.__bbands.getUpperBand()[-1]
        middle_band = self.__bbands.getMiddleBand()[-1]

        if lower_band is None:
            return

        if lower_band is None or upper_band is None or middle_band is None:
            return

        # Ensure there's enough data in the price series
        if len(self.__pricesA) < 1 or len(self.__pricesB) < 1:
            return

        # Spread = PriceA - PriceB

        shares_to_trade = 100

        if spread < lower_band and self.__positionA is None:
            self.__positionA = self.enterLong(self.__instrumentA, shares_to_trade, True)
            self.__positionB = self.enterShort(self.__instrumentB, shares_to_trade, True)

        # Short the spread (Short A, Long B)
        elif spread > upper_band and self.__positionA is None:
            self.__positionA = self.enterShort(self.__instrumentA, shares_to_trade, True)
            self.__positionB = self.enterLong(self.__instrumentB, shares_to_trade, True)



         # Check if there are any positions to exit before entering new ones
        if self.__positionA is not None and self.__positionB is not None:
            if (spread > middle_band and self.__positionA.getShares() > 0) or \
               (spread < middle_band and self.__positionA.getShares() < 0):
                self.__positionA.exitMarket()
                self.__positionB.exitMarket()
                self.__positionA = None
                self.__positionB = None
                return  # Return here to avoid entering new positions in the same bar


# Download historical data for both instruments
tickerA = "AAPL"
tickerB = "MSFT"
start = dt.date(2020, 1, 1)
end = dt.date(2022, 1, 1)
yf.download(tickerA, start=start, end=end).to_csv(tickerA + "_data.csv")
yf.download(tickerB, start=start, end=end).to_csv(tickerB + "_data.csv")

def main():
    feed = yahoofeed.Feed(Frequency.DAY)
    feed.addBarsFromCSV(tickerA, tickerA + "_data.csv")
    feed.addBarsFromCSV(tickerB, tickerB + "_data.csv")

    pairs_trading_strategy = PairsTradingStrategy(feed, tickerA, tickerB, 20, 2)
    splt = plotter.StrategyPlotter(pairs_trading_strategy)
    pairs_trading_strategy.run()
    splt.plot()





if __name__ == "__main__":
    main()
