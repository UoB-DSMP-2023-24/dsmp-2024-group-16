import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast

# 定义函数以安全方式从字符串中提取第一个价格信息
def extract_first_price(data_column):
    first_prices = []
    for item in data_column:
        if item:  # 检查列表是否为空
            orders = ast.literal_eval(item)  # 安全地将字符串解析为列表
            if orders:  # 检查列表是否有元素
                first_prices.append(orders[0][0])  # 添加列表中第一个元素的价格
    return first_prices

# 文件夹路径
folder_path = 'lobs_par'

# 初始化列表来存储每天的价格差均值
price_diff_means = []
dates = []

# 遍历文件夹中的所有文件
for file_name in sorted(os.listdir(folder_path)):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path)
        date = file_name.split('_')[2]
        dates.append(date)

        # 仅当Bid和Ask都非空时，才提取价格
        first_bid_prices = []
        first_ask_prices = []
        for bid, ask in zip(data['Bid'], data['Ask']):
            if bid and ask:  # 确保两者都非空
                bid_orders = ast.literal_eval(bid)
                ask_orders = ast.literal_eval(ask)
                if bid_orders and ask_orders:  # 检查两个列表都有元素
                    first_bid_prices.append(bid_orders[0][0])
                    first_ask_prices.append(ask_orders[0][0])

        # 现在我们可以确信两个列表有相同的长度
        price_diffs = np.array(first_ask_prices) - np.array(first_bid_prices)
        price_diff_means.append(np.mean(price_diffs))

# 现在我们有了每天的价格差均值，可以绘制图表
plt.figure(figsize=(10, 5))  # 根据需要调整尺寸
plt.plot(dates, price_diff_means, marker='o')  # 根据需要添加标记
plt.title('Average Daily Price Difference (First Bid vs. First Ask)')
plt.ylabel('Average Price Difference')
plt.xlabel('Date')
plt.xticks(rotation=90)  # 旋转日期标签以适应
plt.tight_layout()  # 自动调整子图参数以给定填充
plt.show()
