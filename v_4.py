from flask import Flask, render_template, request
from binance.client import Client
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Binance API credentials
API_KEY = 'your_binance_api_key'
API_SECRET = 'your_binance_api_secret'
client = Client(API_KEY, API_SECRET)

def get_btc_price():
    """Fetch the current BTC price from Binance."""
    ticker = client.get_symbol_ticker(symbol="BTCUSDT")
    return float(ticker['price'])

def get_historical_data(symbol, interval='1d', lookback='365d'):
    """Fetch historical price data for the given symbol."""
    klines = client.get_historical_klines(symbol, interval, lookback)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df['close'] = df['close'].astype(float)
    return df['close']

def calculate_volatility(prices, window=14):
    """Calculate volatility using a rolling standard deviation."""
    return prices.pct_change().rolling(window).std() * np.sqrt(window)

def trading_strategy(btc_price, initial_investment, capital, pruning_ratio, stop_loss_threshold, highest_price, trailing_stop_enabled=True):
    """Execute the pruning trading strategy with refined logic and error checks."""
    # Ensure pruning ratios sum to 1
    if sum(pruning_ratio) != 1.0:
        pruning_ratio = tuple(r / sum(pruning_ratio) for r in pruning_ratio)

    # Update trailing stop-loss if applicable
    if btc_price > highest_price:
        highest_price = btc_price
    trailing_stop_price = highest_price * (1 - stop_loss_threshold) if trailing_stop_enabled else initial_investment * (1 - stop_loss_threshold)

    # Pruning logic in bullish market
    if btc_price > initial_investment:
        profit = btc_price - initial_investment
        usdt_pruning, usdc_pruning, bnb_pruning = [profit * ratio for ratio in pruning_ratio]
        capital += usdt_pruning
        portfolio_value = capital + (btc_price - initial_investment)
        message = f"Pruning executed: Added {usdt_pruning} USDT, {usdc_pruning} USDC, {bnb_pruning} BNB"
    
    # Stop-loss in bearish market
    elif btc_price < trailing_stop_price:
        capital *= (1 - stop_loss_threshold)
        portfolio_value = capital
        message = f"Stop-loss triggered: New capital is {capital}"
    
    else:
        portfolio_value = capital
        message = "No action taken"

    return capital, portfolio_value, highest_price, message

def backtest_strategy(initial_capital, pruning_ratio, stop_loss_threshold):
    """Backtest the trading strategy on historical BTC price data...."""
    historical_prices = get_historical_data('BTCUSDT')
    volatility = calculate_volatility(historical_prices)
    
    capital = initial_capital
    initial_investment = initial_capital
    highest_price = historical_prices.iloc[0]
    capital_history = []
    portfolio_history = []
    messages = []
    
    for date, btc_price in historical_prices.iteritems():
        # Volatility filter
        if volatility.loc[date] > 0.05:  # Skip high-volatility days
            capital_history.append(capital)
            portfolio_history.append(capital)
            messages.append(f"{date}: High volatility, no action taken")
            continue

        capital, portfolio_value, highest_price, message = trading_strategy(
            btc_price, initial_investment, capital, pruning_ratio, stop_loss_threshold, highest_price
        )
        
        capital_history.append(capital)
        portfolio_history.append(portfolio_value)
        messages.append(f"{date}: {message}")

    # Plotting results
    plt.figure(figsize=(12, 6))
    plt.plot(historical_prices.index, historical_prices, label="BTC Price")
    plt.plot(historical_prices.index, capital_history, label="Capital Over Time")
    plt.plot(historical_prices.index, portfolio_history, label="Portfolio Value Over Time")
    plt.title("Backtest Results")
    plt.xlabel("Date")
    plt.ylabel("Value (USDT)")
    plt.legend()
    plt.show()

    final_capital = capital_history[-1]
    final_portfolio_value = portfolio_history[-1]
    print(f"Final Capital: {final_capital}")
    print(f"Final Portfolio Value: {final_portfolio_value}")
    print(f"Total Return: {((final_portfolio_value - initial_capital) / initial_capital) * 100:.2f}%")
    return capital_history, portfolio_history, messages

@app.route('/', methods=['GET', 'POST'])
def index():
    """Home page and trading execution."""
    if request.method == 'POST':
        initial_capital = float(request.form['initial_capital'])
        pruning_ratio = (
            float(request.form['usdt_ratio']),
            float(request.form['usdc_ratio']),
            float(request.form['bnb_ratio']),
        )
        stop_loss_threshold = float(request.form['stop_loss'])
        
        # Get current
