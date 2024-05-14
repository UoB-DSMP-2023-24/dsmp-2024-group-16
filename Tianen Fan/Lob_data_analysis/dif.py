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
folder_path = 'lobs_par_test'

# 初始化列表来存储每天的价格差均值
price_diff_means = []
dates = []

# 遍历文件夹中的所有文件
for file_name in sorted(os.listdir(folder_path)):
    # 确保处理的是CSV文件
    if file_name.endswith('.csv'):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, file_name)
        # 读取CSV文件
        data = pd.read_csv(file_path)
        # 提取日期作为键
        date = file_name.split('_')[2]  # 根据实际文件名结构调整
        dates.append(date)  # 添加日期到列表
        # 提取第一个买单和卖单的价格
        first_bid_prices = extract_first_price(data['Bid'])
        first_ask_prices = extract_first_price(data['Ask'])
        # 计算价格差的均值
        price_diffs = np.array(first_ask_prices) - np.array(first_bid_prices)
        price_diff_means.append(np.mean(price_diffs))  # 添加均值到列表

# 现在我们有了每天的价格差均值，可以绘制图表
plt.figure(figsize=(10, 5))  # 根据需要调整尺寸
plt.plot(dates, price_diff_means, marker='o')  # 根据需要添加标记
plt.title('Average Daily Price Difference (First Bid vs. First Ask)')
plt.ylabel('Average Price Difference')
plt.xlabel('Date')
plt.xticks(rotation=90)  # 旋转日期标签以适应
plt.tight_layout()  # 自动调整子图参数以给定填充
plt.show()
