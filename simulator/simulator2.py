import pandas as pd
from datetime import datetime, timedelta

# Load the datasets


import pandas as pd
from datetime import datetime, timedelta

# Load the datasets
predicted_tape_path = '../predicted_tape.csv'
real_tape_path = '../Tapes/UoB_Set01_2025-01-02tapes.csv'
lob_dataset_path = '../lob.csv'

predicted_tape = pd.read_csv(predicted_tape_path)
real_tape = pd.read_csv(real_tape_path, header=None, names=['timestamp', 'price', 'quantity'])
lob_dataset = pd.read_csv(lob_dataset_path)

# Correcting the 'Timestamp' column name in the LOB dataset
lob_dataset.rename(columns={'Timestamp': 'timestamp'}, inplace=True)

# Ensure the timestamp in the LOB dataset is in the correct datetime format
# If the timestamp is not already in datetime format and needs to be aligned with a specific date
lob_dataset['timestamp'] = pd.to_datetime(lob_dataset['timestamp'])

# Convert Real Tape's timestamps
base_date = datetime(2025, 1, 2)
real_tape['datetime'] = real_tape['timestamp'].apply(lambda x: base_date + timedelta(seconds=x))
real_tape.drop(columns=['timestamp'], inplace=True)

# Merge the Real Tape and LOB Dataset
merged_dataset = pd.merge_asof(lob_dataset.sort_values('timestamp'),
                               real_tape.sort_values('datetime'),
                               left_on='timestamp',
                               right_on='datetime',
                               direction='nearest')

# Trading Simulation Setup
initial_capital = 10000
trade_size = 1  # Assume trading 1 share/contract per trade
transaction_cost = 0  # Assume $0 transaction costs for simplicity

capital = initial_capital
holdings = 0  # Number of shares/contracts held
trades = []

# Trading Simulation Logic
for i in range(len(merged_dataset) - 1):
    current_price = merged_dataset.loc[i, 'price']
    next_price = merged_dataset.loc[i + 1, 'price']

    if next_price > current_price and capital >= current_price:
        capital -= (current_price + transaction_cost)
        holdings += trade_size
        trades.append(('Buy', current_price))
    elif next_price < current_price and holdings > 0:
        capital += (current_price - transaction_cost)
        holdings -= trade_size
        trades.append(('Sell', current_price))

if holdings > 0:
    final_price = merged_dataset.iloc[-1]['price']
    capital += holdings * final_price
    trades.append(('Sell', final_price))
    holdings = 0

final_capital = capital
profit_or_loss = final_capital - initial_capital

# Results
print(f"Final Capital: {final_capital}")
print(f"Profit or Loss: {profit_or_loss}")
print(f"Sample Trades: {trades[:10]}")
