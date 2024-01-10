from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.bar import Frequency
from pyalgotrade.stratanalyzer import returns
import pyalgotrade.plotter as plotter
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades
from strategies import SMAStrategy, RSIStrategy, StochStrategy, PairsTradingStrategy

def run_strategy(StrategyClass, csv_file, ticker, initial_cash, *strategy_args):
    feed = yahoofeed.Feed(Frequency.DAY)
    feed.addBarsFromCSV(ticker, csv_file)

    my_strategy = StrategyClass(feed, *strategy_args)
    my_strategy.getBroker().setCash(initial_cash)
    
    # Attach analyzers
    retAnalyzer = returns.Returns()
    my_strategy.attachAnalyzer(retAnalyzer)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    my_strategy.attachAnalyzer(sharpeRatioAnalyzer)
    drawDownAnalyzer = drawdown.DrawDown()
    my_strategy.attachAnalyzer(drawDownAnalyzer)
    tradesAnalyzer = trades.Trades()
    my_strategy.attachAnalyzer(tradesAnalyzer)

    #Plot and run strategy 
    splt = plotter.StrategyPlotter(my_strategy)

    if StrategyClass == SMAStrategy:
        splt.getInstrumentSubplot(ticker).addDataSeries("Fast MA", my_strategy.getSMAFast())
        splt.getInstrumentSubplot(ticker).addDataSeries("Slow MA", my_strategy.getSMASlow())
        my_strategy.run()
        splt.savePlot("plot.png", dpi=None, format='png', fromDateTime=None, toDateTime=None)
        print("-------------------------------------")
        print("SMA STATISTICS")

    elif StrategyClass == RSIStrategy:
        RSI_subplot = splt.getOrCreateSubplot("RSI")
        RSI_subplot.addDataSeries("RSI", my_strategy.getRSI())
        RSI_subplot.addLine("30", 30)
        RSI_subplot.addLine("70", 70)
        my_strategy.run()
        splt.savePlot("plot2.png", dpi=None, format='png', fromDateTime=None, toDateTime=None)
        print("-------------------------------------")
        print("RSI STATISTICS")

    elif StrategyClass == StochStrategy: 
        stochastics_subplot = splt.getOrCreateSubplot("Stochastics")
        stochastics_subplot.addDataSeries("Fast K", my_strategy.getK())
        stochastics_subplot.addDataSeries("Slow D", my_strategy.getD())
        stochastics_subplot.addLine("20", 20)
        stochastics_subplot.addLine("80", 80)
        my_strategy.run()
        splt.savePlot("plot3.png", dpi=None, format='png', fromDateTime=None, toDateTime=None)
        print("-------------------------------------")
        print("OS STATISTICS")
   
    print("Final portfolio value: $%.2f" % my_strategy.getResult())
    print("Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
    print("Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
    print("Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
    print("Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))

    print("")
    print("Total trades: %d" % (tradesAnalyzer.getCount()))
    if tradesAnalyzer.getCount() > 0:
        profits = tradesAnalyzer.getAll()
        print("Avg. profit: $%2.f" % (profits.mean()))
        print("Profits std. dev.: $%2.f" % (profits.std()))
        print("Max. profit: $%2.f" % (profits.max()))
        print("Min. profit: $%2.f" % (profits.min()))
        returns1 = tradesAnalyzer.getAllReturns()
        print("Avg. return: %2.f %%" % (returns1.mean() * 100))
        print("Returns std. dev.: %2.f %%" % (returns1.std() * 100))
        print("Max. return: %2.f %%" % (returns1.max() * 100))
        print("Min. return: %2.f %%" % (returns1.min() * 100))

        print("")
        print("Profitable trades: %d" % (tradesAnalyzer.getProfitableCount()))
    if tradesAnalyzer.getProfitableCount() > 0:
        profits = tradesAnalyzer.getProfits()
        print("Avg. profit: $%2.f" % (profits.mean()))
        print("Profits std. dev.: $%2.f" % (profits.std()))
        print("Max. profit: $%2.f" % (profits.max()))
        print("Min. profit: $%2.f" % (profits.min()))
        returns1 = tradesAnalyzer.getPositiveReturns()
        print("Avg. return: %2.f %%" % (returns1.mean() * 100))
        print("Returns std. dev.: %2.f %%" % (returns1.std() * 100))
        print("Max. return: %2.f %%" % (returns1.max() * 100))
        print("Min. return: %2.f %%" % (returns1.min() * 100))

        print("")
        print("Unprofitable trades: %d" % (tradesAnalyzer.getUnprofitableCount()))
    if tradesAnalyzer.getUnprofitableCount() > 0:
        losses = tradesAnalyzer.getLosses()
        print("Avg. loss: $%2.f" % (losses.mean()))
        print("Losses std. dev.: $%2.f" % (losses.std()))
        print("Max. loss: $%2.f" % (losses.min()))
        print("Min. loss: $%2.f" % (losses.max()))
        returns1 = tradesAnalyzer.getNegativeReturns()
        print("Avg. return: %2.f %%" % (returns1.mean() * 100))
        print("Returns std. dev.: %2.f %%" % (returns1.std() * 100))
        print("Max. return: %2.f %%" % (returns1.max() * 100))
        print("Min. return: %2.f %%" % (returns1.min() * 100)) 

    return my_strategy

#feed, instrumentA, instrumentB, window_size, num_std_dev
def run_pairs_strategy ( tickerA, tickerB, initial_cash, windowSize, num_std_dev):
    feed = yahoofeed.Feed(Frequency.DAY)
    feed.addBarsFromCSV(tickerA, tickerA + "_data.csv")
    feed.addBarsFromCSV(tickerB, tickerB + "_data.csv")


    my_strategy = PairsTradingStrategy(feed, tickerA, tickerB, 20, 2)
    splt = plotter.StrategyPlotter(my_strategy)
    my_strategy.getBroker().setCash(initial_cash)

    my_strategy.run()
    splt.plot()
