import ast
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 定义函数以从订单中提取第一个价格，如果为空则返回0
def get_first_price(order_list):
    try:
        return ast.literal_eval(order_list)[0][0] if order_list else 0
    except:
        return 0

# 文件夹路径
folder_path = 'lobs_par'

# 初始化列表来存储日期和对应的价格差异均值
dates = []
price_diff_means = []

# 遍历文件夹中的所有文件
for file_name in sorted(os.listdir(folder_path)):
    # 确保处理的是CSV文件
    if file_name.endswith('.csv'):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, file_name)
        # 读取CSV文件
        data = pd.read_csv(file_path)
        # 提取日期
        date = file_name.split('_')[2]  # 根据实际文件名结构调整
        dates.append(date)
        # 提取第一个买单和卖单价格，如果为空则为0
        first_bid_prices = data['Bid'].apply(get_first_price)
        first_ask_prices = data['Ask'].apply(get_first_price)
        # 计算价格差异，并处理任何可能的空值
        price_diffs = np.nan_to_num(first_ask_prices) - np.nan_to_num(first_bid_prices)
        # 计算当天的价格差异均值
        mean_diff = np.mean(price_diffs)
        price_diff_means.append(mean_diff)

# 绘制均值随日期变化的图
plt.figure(figsize=(15, 5))
plt.plot(dates, price_diff_means, marker='o')
plt.title('Average Price Difference (Ask - Bid) Over Days')
plt.xlabel('Date')
plt.ylabel('Average Price Difference')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
