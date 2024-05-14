import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast


def load_and_process_files(folder_path):
    bid_prices = []
    ask_prices = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            data = pd.read_csv(file_path)

            # 将字符串形式的列表转换为实际的列表
            data['Bid'] = data['Bid'].apply(ast.literal_eval)
            data['Ask'] = data['Ask'].apply(ast.literal_eval)

            # 对每个文件的Bid和Ask价格进行处理，只统计连续出现的价格为一次
            last_bid_price = None
            last_ask_price = None

            for _, row in data.iterrows():
                if row['Bid']:
                    current_bid_price = row['Bid'][0][0]
                    if current_bid_price != last_bid_price:
                        bid_prices.append(current_bid_price)
                        last_bid_price = current_bid_price

                if row['Ask']:
                    current_ask_price = row['Ask'][0][0]
                    if current_ask_price != last_ask_price:
                        ask_prices.append(current_ask_price)
                        last_ask_price = current_ask_price

    return bid_prices, ask_prices


def plot_frequency_and_distribution(prices, title, color):
    # 转换为numpy数组
    prices_array = np.array(prices)

    # 绘制频率图
    plt.hist(prices_array, bins=30, density=True, alpha=0.6, color=color)

    # 绘制正态分布估计
    mean = np.mean(prices_array)
    std_dev = np.std(prices_array)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = np.exp(-np.power(x - mean, 2) / (2 * std_dev ** 2)) / (np.sqrt(2 * np.pi) * std_dev)
    plt.plot(x, p, 'k', linewidth=2)
    plt.title(title)
    plt.xlabel('Price')
    plt.ylabel('Frequency')


# 文件夹路径
folder_path = 'lobs_par'

# 加载和处理文件
bid_prices, ask_prices = load_and_process_files(folder_path)

# 绘图
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plot_frequency_and_distribution(bid_prices, 'Bid Prices Frequency and Estimated Normal Distribution', 'blue')

plt.subplot(1, 2, 2)
plot_frequency_and_distribution(ask_prices, 'Ask Prices Frequency and Estimated Normal Distribution', 'red')

plt.tight_layout()
plt.show()
