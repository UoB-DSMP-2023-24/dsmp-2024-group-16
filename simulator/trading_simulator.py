import pandas as pd
import ast  # To safely evaluate string representation of lists


# Load the datasets
tape_data = pd.read_csv('../Arima/arima_101_predictions.csv')
lob_data = pd.read_csv('../merge/merged_lob.csv')

# Display the first few rows of each dataset to understand their structure
tape_data.head(), lob_data.head()

# Convert 'timestamp' in tape_data to seconds since the start of the day
tape_data['timestamp'] = pd.to_datetime(tape_data['timestamp'])
tape_data['timestamp_seconds'] = tape_data['timestamp'].dt.hour * 3600 + tape_data['timestamp'].dt.minute * 60 + tape_data['timestamp'].dt.second


def momentum_trading_with_pointers(tape_data, lob_data, initial_capital):
    capital = initial_capital
    position = 0  # No position initially

    tape_index = 0
    lob_index = 0
    tape_len = len(tape_data)
    lob_len = len(lob_data)

    while tape_index < tape_len - 1 and lob_index < lob_len:
        # Current positions in both datasets
        tape_ts = tape_data['timestamp_seconds'].iloc[tape_index]
        lob_ts = lob_data['Timestamp'].iloc[lob_index]

        # Move LOB pointer to match or exceed tape timestamp
        # while lob_index < lob_len - 1 and lob_data['Timestamp'].iloc[lob_index + 1] <= tape_ts:
        #     lob_index += 1
        if lob_index < lob_len - 1 and lob_ts <= tape_ts:
            lob_index += 1
        elif tape_data['timestamp_seconds'].iloc[tape_index + 1] > lob_data['Timestamp'].iloc[lob_index] > tape_ts:

            # If timestamps match, execute trading logic
            # if lob_ts == tape_ts:
            current_price = tape_data['transaction_price'].iloc[tape_index]
            next_price = tape_data['transaction_price'].iloc[tape_index + 1] if tape_index + 1 < tape_len else current_price

            # Parse bid and ask lists
            current_bids = ast.literal_eval(lob_data['Bid'].iloc[lob_index])
            current_asks = ast.literal_eval(lob_data['Ask'].iloc[lob_index])

            # Determine the best bid and ask
            if current_bids:
                best_bid = max(current_bids, key=lambda x: x[0])
                best_bid_price, best_bid_volume = best_bid
            else:
                best_bid_price, best_bid_volume = 0, 0

            if current_asks:
                best_ask = min(current_asks, key=lambda x: x[0])
                best_ask_price, best_ask_volume = best_ask
            else:
                best_ask_price, best_ask_volume = float('inf'), 0

            # Buy if predicted next price is higher than current and best ask
            if next_price > current_price and next_price > best_ask_price:
                buy_volume = 1  # Simplified to always trade one unit
                capital -= buy_volume * best_ask_price
                position += buy_volume

            # Sell if predicted next price is lower than current and best bid
            elif next_price < current_price and position > 0 and best_bid_price > next_price:
                sell_volume = 1  # Simplified to always trade one unit
                capital += sell_volume * best_bid_price
                position -= sell_volume

            lob_index += 1
        else:
            tape_index += 1
    print("shabi")
    # Final sell off all positions at last known bid price
    if position > 0 and ast.literal_eval(lob_data['Bid'].iloc[lob_index]):
        final_bid = max(ast.literal_eval(lob_data['Bid'].iloc[lob_index]), key=lambda x: x[0])
        final_price = final_bid[0]
        capital += position * final_price

    return capital


initial_capital = 10000  # For example, $10,000

# Run the improved trading simulator with the double pointer approach
final_capital = momentum_trading_with_pointers(tape_data, lob_data, initial_capital)
print(final_capital)