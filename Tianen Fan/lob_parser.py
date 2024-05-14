import json
import pandas as pd
import warnings

def parse_lob(data_str):
    timestamps = []
    bids = []
    asks = []

    for i in range(len(data_str)):
        data_str_line = data_str[i].replace('Exch0', '"Exch0"')
        data_str_line = data_str_line.replace("'bid'", '"bid"')
        data_str_line = data_str_line.replace("'ask'", '"ask"')

        data_list = json.loads(data_str_line)

        # Extract exchange rate and exchange name
        exchange_rate = data_list[0]

        # Extract bid and ask data
        bid_data = data_list[2][0][1]
        ask_data = data_list[2][1][1]

        timestamps.append(exchange_rate)
        bids.append([bid_data])
        asks.append([ask_data])

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)

        # Create DataFrames once after the loop
        df = pd.DataFrame({
            'Timestamp': timestamps,
            'Bid': bids,
            'Ask': asks
        })

    # Concatenate nested lists within DataFrame columns
    df['Bid'] = df['Bid'].apply(lambda x: x[0])
    df['Ask'] = df['Ask'].apply(lambda x: x[0])

    return df

# Specify the path to your text file, path记得自己改一下
file_path = 'LOBs/UoB_Set01_2025-01-02LOBs.txt'

# Example usage:
with open(file_path, 'r') as file:
    data_str = file.readlines()

result_df = parse_lob(data_str)
result_df.to_csv('result.csv')
print(result_df[:20])
