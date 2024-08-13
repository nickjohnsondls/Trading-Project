from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.bar import Frequency
from pyalgotrade.stratanalyzer import returns, sharpe, drawdown, trades
import pyalgotrade.plotter as plotter
from strategies import SMAStrategy, RSIStrategy, StochStrategy, PairsTradingStrategy

def run_strategy(StrategyClass, tickers, csv_files, initial_cash, *strategy_args):
    feed = yahoofeed.Feed(Frequency.DAY)
    
    # Add bars for each ticker
    for ticker, csv_file in zip(tickers, csv_files):
        feed.addBarsFromCSV(ticker, csv_file)
    
    # Initialize strategy
    if StrategyClass == PairsTradingStrategy:
        my_strategy = StrategyClass(feed, *tickers, *strategy_args)
    else:
        my_strategy = StrategyClass(feed, *strategy_args)
    
    my_strategy.getBroker().setCash(initial_cash)
    
    # Attach analyzers
    retAnalyzer = returns.Returns()
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    drawDownAnalyzer = drawdown.DrawDown()
    tradesAnalyzer = trades.Trades()

    for analyzer in [retAnalyzer, sharpeRatioAnalyzer, drawDownAnalyzer, tradesAnalyzer]:
        my_strategy.attachAnalyzer(analyzer)

    # Plot and run strategy
    splt = plotter.StrategyPlotter(my_strategy)
    if StrategyClass == SMAStrategy:
        splt.getInstrumentSubplot(tickers[0]).addDataSeries("Fast MA", my_strategy.getSMAFast())
        splt.getInstrumentSubplot(tickers[0]).addDataSeries("Slow MA", my_strategy.getSMASlow())
    elif StrategyClass == RSIStrategy:
        RSI_subplot = splt.getOrCreateSubplot("RSI")
        RSI_subplot.addDataSeries("RSI", my_strategy.getRSI())
        RSI_subplot.addLine("30", 30)
        RSI_subplot.addLine("70", 70)
    elif StrategyClass == StochStrategy:
        stochastics_subplot = splt.getOrCreateSubplot("Stochastics")
        stochastics_subplot.addDataSeries("Fast K", my_strategy.getK())
        stochastics_subplot.addDataSeries("Slow D", my_strategy.getD())
        stochastics_subplot.addLine("20", 20)
        stochastics_subplot.addLine("80", 80)

    my_strategy.run()
    splt.savePlot(f"plot_{StrategyClass.__name__}.png", dpi=None, format='png', fromDateTime=None, toDateTime=None)
    
    # Print statistics
    print("-------------------------------------")
    print(f"{StrategyClass.__name__} STATISTICS")
    print("Final portfolio value: $%.2f" % my_strategy.getResult())
    print("Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
    print("Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
    print("Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
    print("Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))
    print("Total trades: %d" % (tradesAnalyzer.getCount()))

    if tradesAnalyzer.getCount() > 0:
        profits = tradesAnalyzer.getAll()
        print("Avg. profit: $%.2f" % profits.mean())
        print("Profits std. dev.: $%.2f" % profits.std())
        print("Max. profit: $%.2f" % profits.max())
        print("Min. profit: $%.2f" % profits.min())
        returns1 = tradesAnalyzer.getAllReturns()
        print("Avg. return: %.2f %%" % (returns1.mean() * 100))
        print("Returns std. dev.: %.2f %%" % (returns1.std() * 100))
        print("Max. return: %.2f %%" % (returns1.max() * 100))
        print("Min. return: %.2f %%" % (returns1.min() * 100))

    return my_strategy


def plot_pairs_trading_strategy(my_strategy, tickers):
    splt = plotter.StrategyPlotter(my_strategy)
    
    # Plot the spread between the two instruments
    spread_subplot = splt.getOrCreateSubplot("Spread")
    spread_subplot.addDataSeries("Spread", my_strategy.getSpread())
    
    # Plot the spread moving average
    spread_subplot.addDataSeries("Spread MA", my_strategy.getSpreadMA())
    
    # Plot the upper and lower bands (entry/exit points)
    spread_subplot.addDataSeries("Upper Band", my_strategy.getUpperBand())
    spread_subplot.addDataSeries("Lower Band", my_strategy.getLowerBand())

    splt.savePlot(f"plot_PairsTradingStrategy.png", dpi=None, format='png', fromDateTime=None, toDateTime=None)

    # Print statistics directly under pairs trading strategy
    print("-------------------------------------")
    print("PairsTradingStrategy STATISTICS")
    print("Final portfolio value: $%.2f" % my_strategy.getResult())
    print("Cumulative returns: %.2f %%" % (my_strategy.getAnalyzer(returns.Returns()).getCumulativeReturns()[-1] * 100))
    print("Sharpe ratio: %.2f" % (my_strategy.getAnalyzer(sharpe.SharpeRatio()).getSharpeRatio(0.05)))
    print("Max. drawdown: %.2f %%" % (my_strategy.getAnalyzer(drawdown.DrawDown()).getMaxDrawDown() * 100))
    print("Longest drawdown duration: %s" % (my_strategy.getAnalyzer(drawdown.DrawDown()).getLongestDrawDownDuration()))
    print("Total trades: %d" % (my_strategy.getAnalyzer(trades.Trades()).getCount()))

    tradesAnalyzer = my_strategy.getAnalyzer(trades.Trades())
    if tradesAnalyzer.getCount() > 0:
        profits = tradesAnalyzer.getAll()
        print("Avg. profit: $%.2f" % profits.mean())
        print("Profits std. dev.: $%.2f" % profits.std())
        print("Max. profit: $%.2f" % profits.max())
        print("Min. profit: $%.2f" % profits.min())
        returns1 = tradesAnalyzer.getAllReturns()
        print("Avg. return: %.2f %%" % (returns1.mean() * 100))
        print("Returns std. dev.: %.2f %%" % (returns1.std() * 100))
        print("Max. return: %.2f %%" % (returns1.max() * 100))
        print("Min. return: %.2f %%" % (returns1.min() * 100))
