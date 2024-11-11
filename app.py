from flask import Flask, render_template, request, redirect, url_for, session
from binance.client import Client
import pandas as pd
import numpy as np

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

def get_historical_data(symbol, interval='1d', lookback='30d'):
    """Fetch historical price data for the given symbol."""
    klines = client.get_historical_klines(symbol, interval, lookback)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df['close'] = df['close'].astype(float)
    return df['close']

def trading_strategy(initial_capital, pruning_ratio, stop_loss_threshold):
    """Execute the pruning trading strategy with refined logic and error checks."""
    capital = initial_capital
    initial_investment = capital
    btc_price = get_btc_price()
    historical_prices = get_historical_data('BTCUSDT')

    # Ensure pruning ratios sum to 1
    if sum(pruning_ratio) != 1.0:
        pruning_ratio = tuple(r / sum(pruning_ratio) for r in pruning_ratio)

    # Check if pruning or stop-loss should be executed
    if btc_price > initial_investment:
        profit = btc_price - initial_investment
        usdt_pruning, usdc_pruning, bnb_pruning = [profit * ratio for ratio in pruning_ratio]
        capital += usdt_pruning
        historical_prices.loc[pd.Timestamp.now()] = btc_price
        portfolio_value = capital + (btc_price - initial_investment)
        return capital, portfolio_value, f"Pruning executed: Added {usdt_pruning} USDT, {usdc_pruning} USDC, {bnb_pruning} BNB"
    elif btc_price < initial_investment * (1 - stop_loss_threshold):
        capital = capital * (1 - stop_loss_threshold)
        return capital, capital, f"Stop-loss triggered: New capital is {capital}"

    return capital, capital, "No action taken"


@app.route('/', methods=['GET', 'POST'])
def index():
    """Home page and trading execution."""
    if request.method == 'POST':
        initial_capital = float(request.form['initial_capital'])
        pruning_ratio = (float(request.form['usdt_ratio']), float(request.form['usdc_ratio']), float(request.form['bnb_ratio']))
        stop_loss_threshold = float(request.form['stop_loss'])

        capital, portfolio_value, message = trading_strategy(initial_capital, pruning_ratio, stop_loss_threshold)
        return render_template('index.html', capital=capital, portfolio_value=portfolio_value, message=message)
   
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```
