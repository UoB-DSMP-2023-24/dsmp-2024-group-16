import pandas as pd

# Load the CSV file to review its structure and content
file_path = '../Tapes/UoB_Set01_2025-06-23tapes.csv'
data = pd.read_csv(file_path)

# Correcting the DataFrame column names based on the user's clarification
data.columns = ['Timestamp', 'Price', 'Volume']

# Display the corrected DataFrame structure
data.head()

# Define initial setup and constants
initial_capital = 10000


# Revised strategy implementations considering volume constraints

def momentum_trading_revised(data, initial_capital):
    capital = initial_capital
    position = 0  # No position initially

    for i in range(len(data) - 1):
        current_price = data['Price'].iloc[i]
        available_volume = data['Volume'].iloc[i]

        # Buy if next price is higher than current price
        if data['Price'].iloc[i + 1] > current_price:
            max_affordable_volume = capital / current_price
            buy_volume = min(max_affordable_volume, available_volume)
            capital -= buy_volume * current_price
            position += buy_volume
        # Sell if next price is lower than current price
        elif data['Price'].iloc[i + 1] < current_price and position > 0:
            sell_volume = min(position, available_volume)
            capital += sell_volume * current_price
            position -= sell_volume

    # Final sell at the last price to liquidate position
    if position > 0:
        final_price = data['Price'].iloc[-1]
        capital += position * final_price

    return capital


def volume_weighted_strategy_revised(data, initial_capital):
    capital = initial_capital
    position = 0  # No position initially

    for i in range(len(data) - 1):
        current_price = data['Price'].iloc[i]
        available_volume = data['Volume'].iloc[i]

        # Buy signal: price and volume increase
        if data['Price'].iloc[i + 1] > current_price and data['Volume'].iloc[i + 1] > data['Volume'].iloc[i]:
            max_affordable_volume = capital / current_price
            buy_volume = min(max_affordable_volume, available_volume)
            capital -= buy_volume * current_price
            position += buy_volume
        # Sell signal: price decrease and volume increase
        elif data['Price'].iloc[i + 1] < current_price and data['Volume'].iloc[i + 1] > data['Volume'].iloc[
            i] and position > 0:
            sell_volume = min(position, available_volume)
            capital += sell_volume * current_price
            position -= sell_volume

    # Final sell at the last price to liquidate position
    if position > 0:
        final_price = data['Price'].iloc[-1]
        capital += position * final_price

    return capital


# Re-run simulations with volume constraints
momentum_profit_revised = momentum_trading_revised(data, initial_capital)
volume_weighted_profit_revised = volume_weighted_strategy_revised(data, initial_capital)

print(momentum_profit_revised, volume_weighted_profit_revised)
