def calculate_trailing_stop(highest_price, btc_price, stop_loss_threshold):
    """Calculate trailing stop-loss price."""
    return highest_price * (1 - stop_loss_threshold)

def pruning_logic(profit, pruning_ratio):
    """Distribute profits based on pruning ratios."""
    return [profit * ratio for ratio in pruning_ratio]

def trading_strategy(btc_price, state, pruning_ratio, stop_loss_threshold, trailing_stop_enabled=True):
    """Refactored trading strategy."""
    highest_price = max(state['highest_price'], btc_price)
    trailing_stop_price = (
        calculate_trailing_stop(highest_price, btc_price, stop_loss_threshold)
        if trailing_stop_enabled
        else state['initial_investment'] * (1 - stop_loss_threshold)
    )

    if btc_price > state['initial_investment']:  # Bullish market
        profit = btc_price - state['initial_investment']
        usdt_pruning, usdc_pruning, bnb_pruning = pruning_logic(profit, pruning_ratio)
        state['capital'] += usdt_pruning
        state['portfolio_value'] = state['capital'] + (btc_price - state['initial_investment'])
        message = f"Pruning executed: Added {usdt_pruning} USDT, {usdc_pruning} USDC, {bnb_pruning} BNB"

    elif btc_price < trailing_stop_price:  # Bearish market
        state['capital'] *= (1 - stop_loss_threshold)
        state['portfolio_value'] = state['capital']
        message = f"Stop-loss triggered: New capital is {state['capital']}"

    else:  # No action
        state['portfolio_value'] = state['capital']
        message = "No action taken"

    state['highest_price'] = highest_price
    return state, message
