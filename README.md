# BTC Trading Web Application

The **BTC Trading Web Application** is a user-friendly, Flask-based platform designed to automate Bitcoin trading strategies. It integrates with the Binance API to fetch real-time and historical Bitcoin data, enabling users to execute their trading strategies with ease.

## Features

- **Automated Trading**: Executes predefined Bitcoin trading strategies based on user-defined parameters.
- **Real-Time Data**: Fetches live Bitcoin market data and provides real-time updates on trading performance.
- **Customizable Parameters**: Allows users to input key trading parameters such as:
  - Initial investment capital
  - Pruning ratios
  - Stop-loss thresholds
- **Portfolio Tracking**: Monitors and displays updates on capital and portfolio value, giving users full transparency over their investments.
- **User-Friendly Interface**: Simple web interface that makes Bitcoin trading accessible for both beginners and experienced traders.

## How It Works

1. **User Input**: Through the web interface, users specify their trading parameters (e.g., initial capital, pruning ratios, stop-loss levels).
2. **Backend Processing**: The application processes these inputs and applies the selected trading strategy.
3. **Real-Time Monitoring**: As the strategy executes, the backend continuously tracks portfolio performance and updates the user on capital and portfolio value in real-time.
4. **Data Integration**: The app fetches real-time and historical data from the Binance API to inform trading decisions.

## Installation

To get started, clone this repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/btc-trading-web-app.git
cd btc-trading-web-app
pip install -r requirements.txt
