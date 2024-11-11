# BTC Trading Web Application

The BTC Trading Web Application is a Flask-based platform designed to automate Bitcoin trading strategies. It integrates with the Binance API to fetch real-time and historical Bitcoin data, enabling users to execute and backtest trading strategies with ease. The app is optimized for both spot and futures trading.

---

## Features
- **Automated Trading**: Executes predefined Bitcoin trading strategies based on user-defined parameters.
- **Real-Time Data**: Fetches live Bitcoin market data and provides real-time updates on trading performance.
- **Customizable Parameters**: Users can input key trading parameters such as:
  - Initial investment capital
  - Pruning ratios for asset allocation (USDT, USDC, BNB)
  - Stop-loss thresholds
- **Portfolio Tracking**: Monitors and displays updates on capital and portfolio value, giving users full transparency over their investments.
- **Backtesting**: Run backtests using historical Bitcoin price data to evaluate trading strategies.
- **Volatility Filters**: Optionally filters high-volatility periods during backtesting.
- **Trailing Stop-Loss**: A trailing stop-loss feature that adjusts dynamically based on the highest price observed during the trade.
- **Spot and Futures Trading**: Supports both spot and futures markets for trading Bitcoin.
- **User-Friendly Interface**: A simple web interface that makes Bitcoin trading accessible for both beginners and experienced traders.

---

## How It Works

1. **User Input**: 
   - Users specify their trading parameters via the web interface (e.g., initial capital, pruning ratios, stop-loss thresholds).
   
2. **Backend Processing**: 
   - The app uses the provided inputs to execute the selected trading strategy, making real-time decisions based on Bitcoin market conditions.
   
3. **Real-Time Monitoring**: 
   - The backend continuously monitors portfolio performance and updates the user on capital and portfolio value.
   
4. **Data Integration**: 
   - Real-time and historical data is fetched from the Binance API to inform trading decisions.
   
5. **Backtesting**: 
   - The app also supports backtesting of strategies on historical price data to assess performance before going live.

---

## Installation

To get started, clone this repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/btc-trading-web-app.git
cd btc-trading-web-app
pip install -r requirements.txt
