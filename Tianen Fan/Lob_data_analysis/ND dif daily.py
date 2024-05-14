import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取Excel文件
file_path = 'lobs_par/UoB_Set01_2025-01-02LOBs.csv'
data = pd.read_csv(file_path)

# 提取买入价和卖出价中的第一项价格数据
bid_prices = []
ask_prices = []
for index, row in data.iterrows():
    if row['Bid'] != '[]':
        bid_prices.append(eval(row['Bid'])[0][0])
    if row['Ask'] != '[]':
        ask_prices.append(eval(row['Ask'])[0][0])

# 确保买入价和卖出价列表长度一致
min_length = min(len(bid_prices), len(ask_prices))
bid_prices = bid_prices[:min_length]
ask_prices = ask_prices[:min_length]

# 计算价格差值的绝对值
price_diff_abs = [abs(b - a) for b, a in zip(bid_prices, ask_prices)]

# 将差值数据转换为DataFrame以便分析
price_diff_df = pd.DataFrame(price_diff_abs, columns=['Price Difference'])



# 绘制价格差值的绝对值分布图
plt.figure(figsize=(10, 6))
sns.histplot(price_diff_df['Price Difference'], kde=True, bins=30)
plt.title('Ask and Bid dif Prices Histogram')
plt.xlabel('ask-bid-dif')
plt.ylabel('frequency')
plt.show()
