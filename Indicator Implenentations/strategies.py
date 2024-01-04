from pyalgotrade import strategy
from pyalgotrade.technical import ma, rsi, stoch

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
           ## THIS IS WHERE YOU WILL IMPLEMENT MACHINE LEARNING
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

