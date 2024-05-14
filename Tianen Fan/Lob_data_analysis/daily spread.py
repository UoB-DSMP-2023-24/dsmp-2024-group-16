import pandas as pd
import matplotlib.pyplot as plt
import ast

# Load the data from CSV
df = pd.read_csv('result.csv')

# Function to parse the list and extract the first value if available
def parse_and_diff(lst_str_bid, lst_str_ask):
    bid_list = ast.literal_eval(lst_str_bid)
    ask_list = ast.literal_eval(lst_str_ask)
    if bid_list and ask_list:  # If both lists are not empty
        bid_first = bid_list[0][0]  # Extract the first value of the bid
        ask_first = ask_list[0][0]  # Extract the first value of the ask
        return ask_first - bid_first  # Return the difference
    return None  # Return None if either list is empty

# Apply the function to each row to calculate the difference
df['Price_diff'] = df.apply(lambda row: parse_and_diff(row['Bid'], row['Ask']), axis=1)

# Drop rows where 'Price_diff' is None
df_diff_cleaned = df.dropna(subset=['Price_diff'])

# Plotting with adjusted marker size
plt.figure(figsize=(12, 6))
plt.plot(df_diff_cleaned['Timestamp'], df_diff_cleaned['Price_diff'], label='Ask-Bid Difference', marker='o', linestyle='-', color='purple', markersize=4)  # Adjusted marker size

# Adding plot details
plt.title('Difference Between First Ask and Bid Values Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Price Difference')
plt.legend()
plt.grid(True)

plt.show()
