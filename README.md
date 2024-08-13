Quantitative Trading Strategy Backtest Project
Overview
This project involves the backtesting of four different trading strategies using historical stock data obtained from Yahoo Finance through the yfinance library. The strategies tested include:

Simple Moving Average (SMA) Strategy
Relative Strength Index (RSI) Strategy
Stochastic Oscillator (Stoch OS) Strategy
Pairs Trading Strategy
The backtest period spans from 2019 to 2024, and the data has been saved in CSV format for analysis.

Project Structure
Main Files:
The core of the project, including the primary backtests and implementations, are located here. This includes the setup of the strategies, the application of the strategies to the historical data, and the calculation of key performance metrics such as final portfolio value, cumulative returns, Sharpe ratio, and drawdowns.
Extra Plots:
This directory contains additional visualizations created during the analysis, such as time series plots of stock prices with overlaid signals from the various strategies, and portfolio value over time.
Strategies from Scratch:
These implementations are built without relying on yfinance. They focus on the raw application of the strategies to the data, allowing for a deeper understanding of how each strategy operates under different market conditions.
Results Summary
SMA Strategy
Final Portfolio Value: $93,142.64
Cumulative Returns: 831.43%
Sharpe Ratio: 1.03
Max Drawdown: 58.40%
Total Trades: 2
RSI Strategy
Final Portfolio Value: $38,820.39
Cumulative Returns: 288.20%
Sharpe Ratio: 0.80
Max Drawdown: 47.37%
Total Trades: 6
Stochastic Oscillator (Stoch OS) Strategy
Final Portfolio Value: $23,326.99
Cumulative Returns: 133.27%
Sharpe Ratio: 0.50
Max Drawdown: 52.81%
Total Trades: 55
Pairs Trading Strategy
Final Portfolio Value: $11,436.75
Cumulative Returns: 14.37%
Sharpe Ratio: 0.16
Max Drawdown: 34.48%
Total Trades: 68
Next Steps
Risk Management Improvement
Enhance Stop-Loss Mechanisms: Implement and test stop-loss orders to reduce the impact of large drawdowns, particularly in the SMA and RSI strategies.
Position Sizing Adjustments: Optimize position sizes to ensure adequate cash reserves are available, reducing the occurrence of missed trades due to insufficient funds.
Strategy Diversification: Combine multiple strategies in a portfolio context to balance out risk and improve overall returns.
Volatility-Based Adjustments: Consider using volatility-adjusted versions of these strategies to dynamically adapt to changing market conditions.
By refining these strategies with improved risk management, it is possible to achieve a more stable and consistent performance across different market environments.



<img width="346" alt="Screenshot 2024-08-13 at 3 24 27 PM" src="https://github.com/user-attachments/assets/3c7266ad-86d8-4701-85c1-1c1fdefee44d">
