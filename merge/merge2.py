import pandas as pd
import ast


# Function to parse the 'Bid' and 'Ask' columns from string representation to lists
def parse_bid_ask_columns(row):
    row['Bid'] = ast.literal_eval(row['Bid'])
    row['Ask'] = ast.literal_eval(row['Ask'])
    return row


# Load the tape data
tape_data_path = 'tape_short.csv'
tape_data = pd.read_csv(tape_data_path, header=None)
tape_data.columns = ['Timestamp', 'Price', 'Volume']

# Load the LOB data
lob_data_path = 'lob_short.csv'
lob_data = pd.read_csv(lob_data_path)

# Apply the parsing function to the LOB data
lob_data = lob_data.apply(parse_bid_ask_columns, axis=1)

# Convert LOB data to a list of dictionaries for easier manipulation
lob_data_list = lob_data.to_dict('records')


# Function to find the index in the LOB data where a new row should be inserted
def find_insert_index(timestamp):
    for i, row in enumerate(lob_data_list):
        if timestamp < row['Timestamp']:
            return i
    return len(lob_data_list)


# Adjust the tape data to ensure 'Price' and 'Volume' are integers
tape_data['Price'] = tape_data['Price'].astype(int)
tape_data['Volume'] = tape_data['Volume'].astype(int)


# Now, let's proceed with the merging operation as before, ensuring the data types match.
# The rest of the code remains the same.

# Function to update or insert a row based on tape transaction, now ensuring data types match
def merge_transaction(transaction):
    global lob_data_list
    timestamp, price, volume = transaction
    price = int(price)
    volume = int(volume)
    inserted = False

    # Check if there's a matching timestamp and update accordingly
    for row in lob_data_list:
        if row['Timestamp'] == timestamp:
            # Check bids and asks for the price, now correctly matching integers
            if any(bid[0] == price for bid in row['Bid']):
                row['Ask'].insert(0, [price, volume])
            elif any(ask[0] == price for ask in row['Ask']):
                row['Bid'].insert(0, [price, volume])
            inserted = True
            break

    # If no matching timestamp, insert a new row
    if not inserted:
        insert_index = find_insert_index(timestamp)
        new_row = {
            'Timestamp': timestamp,
            'Bid': [[price, volume]] + (lob_data_list[insert_index - 1]['Bid'] if insert_index > 0 else []),
            'Ask': [[price, volume]] + (lob_data_list[insert_index - 1]['Ask'] if insert_index > 0 else [])
        }
        lob_data_list.insert(insert_index, new_row)


# Iterate through each transaction in the tape data and merge, with correct data types
for index, transaction in tape_data.iterrows():
    merge_transaction(transaction)

# Convert the updated LOB data back to a DataFrame
updated_lob_df = pd.DataFrame(lob_data_list)

updated_lob_df.to_csv('merged_lob2.csv', index=False)