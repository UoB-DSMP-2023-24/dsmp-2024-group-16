
# the simple idea would be buy low sell high, the first thing to note is that
# for a given time period, the low might appear after high.
# so what we need is the biggest rise in price

# useless gpt generated garbage


import pandas as pd
import ast  # Importing for safe string literal evaluation

# Load the data from CSV files
predicted_tape = pd.read_csv('../predicted_tape.csv')
real_tape = pd.read_csv('../../Tapes/UoB_Set01_2025-01-02tapes.csv', header=None, names=['timestamp', 'price', 'quantity'])
lob = pd.read_csv('../../lob_full.csv')

# We need to convert the 'Bid' and 'Ask' columns from string representations of lists to actual lists
lob['Bid'] = lob['Bid'].apply(ast.literal_eval)
lob['Ask'] = lob['Ask'].apply(ast.literal_eval)

# Initialize variables
cash = 1000000  # Starting cash
position = 0  # Starting position (number of shares owned)
transaction_costs = 0.001  # Assuming a 0.1% transaction cost for simplicity

# Trading simulation
for index, row in real_tape.iterrows():
    timestamp = row['timestamp']
    current_price = row['price']

    # Predicted future price from predicted tape
    predicted_price = predicted_tape.iloc[index]['transaction_price']

    # Check if there are bids and asks in the LOB
    current_bids = lob.iloc[index]['Bid']
    current_asks = lob.iloc[index]['Ask']

    # If there are bids and asks available, get the best bid and ask
    current_bid = current_bids[0][0] if current_bids else None
    current_ask = current_asks[0][0] if current_asks else None

    # Buy if predicted price is higher than current ask and there is an ask available
    if current_ask and predicted_price > current_ask and cash >= current_ask:
        # Assuming we buy at the best ask price and the quantity available there
        quantity = min(position + current_asks[0][1], cash // current_ask)
        position += quantity
        cash -= quantity * current_ask * (1 + transaction_costs)

    # Sell if we own the asset and predicted price is lower than current bid and there is a bid available
    if current_bid and position > 0 and predicted_price < current_bid:
        # Assuming we sell at the best bid price and only the quantity we own
        quantity = min(position, current_bids[0][1])
        position -= quantity
        cash += quantity * current_bid * (1 - transaction_costs)

# Calculate final value
final_value = cash + position * real_tape.iloc[-1]['price']  # Assuming we liquidate at the last known price

print(f"Final Portfolio Value: {final_value}")
