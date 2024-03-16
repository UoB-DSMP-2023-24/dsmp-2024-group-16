import json
import pandas as pd
import warnings

def parse_lob(data_str):
    lob_data = {}
    for line in data_str:
        line = line.replace('Exch0', '"Exch0"').replace("'bid'", '"bid"').replace("'ask'", '"ask"')
        data = json.loads(line)

        timestamp = data[0]
        bids = data[2][0][1]
        asks = data[2][1][1]

        highest_bid = max(bids, key=lambda x: x[0])[0] if bids else None
        lowest_ask = min(asks, key=lambda x: x[0])[0] if asks else None

        if timestamp not in lob_data:
            lob_data[timestamp] = {'Bid': highest_bid, 'Ask': lowest_ask}
        else:
            if highest_bid and (lob_data[timestamp]['Bid'] is None or highest_bid > lob_data[timestamp]['Bid']):
                lob_data[timestamp]['Bid'] = highest_bid
            if lowest_ask and (lob_data[timestamp]['Ask'] is None or lowest_ask < lob_data[timestamp]['Ask']):
                lob_data[timestamp]['Ask'] = lowest_ask

    df = pd.DataFrame.from_dict(lob_data, orient='index').reset_index().rename(columns={'index': 'Timestamp'})
    return df

file_path = 'C:/Users/Wilson/Desktop/TB2/Dataminiproject/Dataset2/UoB_Set01_2025-01-02LOBs.txt'
with open(file_path, 'r') as file:
    data_str = file.readlines()
result_df = parse_lob(data_str)

result_df.to_csv('result.csv', index=False)

print(result_df.head(20))
