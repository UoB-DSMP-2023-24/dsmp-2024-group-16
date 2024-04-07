import pandas as pd

# Read the newly provided LOB data, adjusting for the updated indexing
lob_csv_path = 'lob_short.csv'
lob_df = pd.read_csv(lob_csv_path, header=None)
lob_df.columns = ['Timestamp', 'Bid', 'Ask']
lob_df['Bid'] = lob_df['Bid'].apply(lambda x: eval(x) if x.startswith('[') else [])
lob_df['Ask'] = lob_df['Ask'].apply(lambda x: eval(x) if x.startswith('[') else [])
lob_df = lob_df.iloc[1:]
lob_df['Timestamp'] = lob_df['Timestamp'].astype(float)

# Correcting tape data reading, including the first row as actual data
tape_csv_path = 'tape_short.csv'
tape_df = pd.read_csv(tape_csv_path, header=None, skiprows=0)
tape_df.columns = ['Timestamp', 'Price', 'Volume']
tape_df['Timestamp'] = tape_df['Timestamp'].astype(float)
tape_df['Price'] = tape_df['Price'].astype(int)
tape_df['Volume'] = tape_df['Volume'].astype(int)

# Initialize a new DataFrame for the merged data
merged_lob_df = pd.DataFrame(columns=['Timestamp', 'Bid', 'Ask'])

# Track the last known state of the LOB for each new timestamp from the tape data
last_known_lob = {'Bid': [], 'Ask': []}

# Iterate through each timestamp in the tape data
for index, tape_row in tape_df.iterrows():
    tape_timestamp = tape_row['Timestamp']
    price_volume_pair = [tape_row['Price'], tape_row['Volume']]

    # If the timestamp is not in the LOB DataFrame, add a new entry
    if tape_timestamp not in lob_df['Timestamp'].values:
        new_bid_list = [price_volume_pair] + last_known_lob['Bid']
        new_ask_list = [price_volume_pair] + last_known_lob['Ask']
        new_lob_entry = {'Timestamp': tape_timestamp, 'Bid': new_bid_list, 'Ask': new_ask_list}
        merged_lob_df = pd.concat([merged_lob_df, pd.DataFrame([new_lob_entry])], ignore_index=True)
    else:
        # Update the last known LOB state from the existing entry in LOB DataFrame
        existing_lob_entry = lob_df[lob_df['Timestamp'] == tape_timestamp].iloc[0]
        last_known_lob['Bid'] = existing_lob_entry['Bid']
        last_known_lob['Ask'] = existing_lob_entry['Ask']

# Append the original LOB entries to the merged DataFrame
merged_lob_df = pd.concat([merged_lob_df, lob_df], ignore_index=True)

# Sort and reset index
merged_lob_df.sort_values(by='Timestamp', inplace=True)
merged_lob_df.reset_index(drop=True, inplace=True)
