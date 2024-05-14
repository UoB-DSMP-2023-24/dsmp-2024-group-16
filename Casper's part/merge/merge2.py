import pandas as pd

# Read the newly provided LOB data, adjusting for the updated indexing
lob_csv_path = '../lob_full2.csv'  # Updated file path

# Reading the updated LOB CSV file into a pandas DataFrame
lob_df = pd.read_csv(lob_csv_path)
lob_df.columns = ['Timestamp', 'Bid', 'Ask']
lob_df['Bid'] = lob_df['Bid'].apply(lambda x: eval(x) if x.startswith('[') else [])
lob_df['Ask'] = lob_df['Ask'].apply(lambda x: eval(x) if x.startswith('[') else [])

# Correcting tape data reading, including the first row as actual data
tape_csv_path = '../Tapes/UoB_Set01_2025-01-02tapes.csv'  # Tape file path remains the same
tape_df = pd.read_csv(tape_csv_path, header=None, skiprows=0)
tape_df.columns = ['Timestamp', 'Price', 'Volume']

tape_df['Price'] = tape_df['Price'].astype(int)
tape_df['Volume'] = tape_df['Volume'].astype(int)


def merge_data(tape_df, lob_df):
    # Initialize merged data list
    merged_data = []
    tape_idx, lob_idx = 0, 0

    while tape_idx < len(tape_df) and lob_idx < len(lob_df):
        # Get the current row of tape and LOB data
        tape_row = tape_df.iloc[tape_idx]
        lob_row = lob_df.iloc[lob_idx]
        bids, asks = lob_row['Bid'], lob_row['Ask']
        price, volume = int(tape_row['Price']), int(tape_row['Volume'])

        if tape_row['Timestamp'] < lob_row['Timestamp']:
            price_in_bid = any(price == bid[0] for bid in merged_data[-1][1])
            price_in_ask = any(price == ask[0] for ask in merged_data[-1][2])
            # Tape data comes before LOB data, insert tape data into new LOB row
            new_bid = [price, volume]
            new_ask = [price, volume]
            new_bids = merged_data[-1][1].copy()
            new_asks = (merged_data[-1][2].copy())
            if price_in_ask:
                new_bids.insert(0, new_bid)
            if price_in_bid:
                new_asks.insert(0, new_ask)
            merged_data.append([tape_row['Timestamp'], new_bids, new_asks])
            tape_idx += 1
        elif tape_row['Timestamp'] == lob_row['Timestamp']:
            # Check for price in bids or asks and adjust accordingly
            price_in_bid = any(price == bid[0] for bid in bids)
            price_in_ask = any(price == ask[0] for ask in asks)
            if price_in_bid:
                # If price is in bid, add transaction to start of ask list
                asks.insert(0, [price, volume])
            if price_in_ask:
                # If price is in ask, add transaction to start of bid list
                bids.insert(0, [price, volume])
            # Add the modified LOB row to merged data
            merged_data.append([lob_row['Timestamp'], bids, asks])
            tape_idx += 1
            lob_idx += 1
        else:
            # LOB data comes before tape data, add LOB data to merged data
            merged_data.append([lob_row['Timestamp'], bids, asks])
            lob_idx += 1

    # Handle remaining data in either dataset
    while tape_idx < len(tape_df):
        tape_row = tape_df.iloc[tape_idx]
        # Assuming inheritance of bid/ask from the last entry of merged_data if available
        last_bids, last_asks = merged_data[-1][1:3] if merged_data else ([], [])
        new_bid = [price, volume]
        new_ask = [price, volume]
        # Insert the transaction at the start of both bid and ask lists
        merged_data.append([tape_row['Timestamp'], [new_bid] + last_bids, [new_ask] + last_asks])
        tape_idx += 1

    while lob_idx < len(lob_df):
        lob_row = lob_df.iloc[lob_idx]
        bids = (lob_row['Bid'])
        asks = (lob_row['Ask'])
        merged_data.append([lob_row['Timestamp'], bids, asks])
        lob_idx += 1

    # Convert the merged data to a DataFrame
    merged_df = pd.DataFrame(merged_data, columns=['Timestamp', 'Bid', 'Ask'])
    return merged_df


# Merge the tape and LOB data into a single DataFrame
merged_df = merge_data(tape_df, lob_df)
merged_df.to_csv('merged_lob.csv', index=False)
