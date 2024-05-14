import json
import pandas as pd
import warnings
import os
from glob import glob

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


# 找到 lobs 文件夹中的所有 txt 文件
file_paths = glob('lobs/*.txt')

for file_path in file_paths:
    # 读取每个文件的数据
    with open(file_path, 'r') as file:
        data_str = file.readlines()

    # 解析数据
    result_df = parse_lob(data_str)

    # 构造输出文件名
    base_name = os.path.basename(file_path)
    csv_file_name = base_name.replace('.txt', '.csv')
    output_path = os.path.join('lobs_par', csv_file_name)

    # 保存结果到 lobs_par 文件夹
    result_df.to_csv(output_path)



