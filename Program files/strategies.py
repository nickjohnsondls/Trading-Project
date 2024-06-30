from pyalgotrade import strategy
from pyalgotrade.technical import ma, rsi, stoch, bollinger
from pyalgotrade.dataseries import SequenceDataSeries

#SMA Strategy
class SMAStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, fast_period, slow_period, ticker):
        super(SMAStrategy, self).__init__(feed)
        self.__position = None
        self.__instrument = ticker
        self.__prices = feed[self.__instrument].getCloseDataSeries()
        self.__fast_ma = ma.SMA(self.__prices, fast_period)
        self.__slow_ma = ma.SMA(self.__prices, slow_period)

    def onBars(self, bars):
        if self.__position is not None:
            if self.exitSignal(bars):
                self.__position.exitMarket()
                self.__position = None
            return

        if self.entrySignal(bars):
            shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getClose())
            self.__position = self.enterLong(self.__instrument, shares)
   
    def entrySignal(self, bars):
     if len(self.__fast_ma) < 2 or len(self.__slow_ma) < 2:
        return False
     if self.__fast_ma[-1] is None or self.__fast_ma[-2] is None or self.__slow_ma[-1] is None or self.__slow_ma[-2] is None:
        return False
     return self.__fast_ma[-1] > self.__slow_ma[-1] and self.__fast_ma[-2] <= self.__slow_ma[-2] 

    def exitSignal(self, bars):
        if len(self.__fast_ma) < 2 or len(self.__slow_ma) < 2:
            return False
        if self.__fast_ma[-1] is None or self.__fast_ma[-2] is None or self.__slow_ma[-1] is None or self.__slow_ma[-2] is None:
            return False
        return self.__fast_ma[-1] < self.__slow_ma[-1] and self.__fast_ma[-2] >= self.__slow_ma[-2] 
    # Accessor methods for plotter
    def getSMAFast(self):
        return self.__fast_ma

    def getSMASlow(self):
        return self.__slow_ma

# RSI Strategy
class RSIStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, rsi_period, ticker):
        super(RSIStrategy, self).__init__(feed)
        self.__position = None
        self.__instrument = ticker
        self.__prices = feed[self.__instrument].getCloseDataSeries()
        self.__rsi = rsi.RSI(self.__prices, rsi_period)

    def onBars(self, bars):
        if self.__position is not None:
            if self.exitSignal(bars):
                self.__position.exitMarket()
                self.__position = None
            return

        if self.entrySignal(bars):
           ## THIS IS WHERE YOU WILL IMPLEMENT MACHINE LEARNING
            shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getClose())
            self.__position = self.enterLong(self.__instrument, shares)

    def entrySignal(self, bars):
        if self.__rsi[-1] is None:
            return False
        return self.__rsi[-1] < 30

    def exitSignal(self, bars):
        if self.__rsi[-1] is None:
            return False
        return self.__rsi[-1] > 70 

    #Access methods for plotter
    def getRSI(self):
        return self.__rsi

#OS Strategy 
class StochStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, fastKPeriod, slowDPeriod, ticker):
        super(StochStrategy, self).__init__(feed)
        self.__position = None
        self.__instrument = ticker
        self.__instrumentSeries = feed[self.__instrument]
        self.__fast_k = stoch.StochasticOscillator(self.__instrumentSeries, fastKPeriod)
        self.__slow_d = stoch.StochasticOscillator(self.__instrumentSeries, slowDPeriod)


    def onBars(self, bars):
        if self.__position is not None:
            if self.exitSignal(bars):
                self.__position.exitMarket()
                self.__position = None
            return

        if self.entrySignal(bars):
           ## THIS IS WHERE YOU WILL IMPLEMENT MACHINE LEARNING
            shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getClose())
            self.__position = self.enterLong(self.__instrument, shares)

    def entrySignal(self, bars):
        if len(self.__fast_k) < 2 or len(self.__slow_d) < 2:
            return False
        if self.__fast_k[-1] is None or self.__fast_k[-2] is None or self.__slow_d[-1] is None or self.__slow_d[-2] is None:
            return False
        return self.__slow_d[-1] < 20 and self.__fast_k[-2] >= self.__slow_d[-2]

    def exitSignal(self, bars):
        if len(self.__fast_k) < 2 or len(self.__slow_d) < 2:
            return False
        if self.__fast_k[-1] is None or self.__fast_k[-2] is None or self.__slow_d[-1] is None or self.__slow_d[-2] is None:
            return False
        return self.__slow_d[-1] > 80 and self.__fast_k[-2] <= self.__slow_d[-2]

    #Access methods for plotter
    def getD(self):
        return self.__slow_d

    def getK(self):
        return self.__fast_k


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
