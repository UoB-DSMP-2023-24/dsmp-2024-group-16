import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取Excel文件
file_path = 'lobs_par/UoB_Set01_2025-01-02LOBs.csv'
data = pd.read_csv(file_path)

# 提取买入价中的第一项价格数据
bid_prices = []
for bid_list in data['Bid']:
    if bid_list != '[]':  # 确保列表不为空
        bid_list_eval = eval(bid_list)  # 将字符串形式的列表转换为实际的列表对象
        bid_prices.append(bid_list_eval[0][0])  # 提取并添加第一项价格数据

# 将价格数据转换为DataFrame以便分析
bid_prices_df = pd.DataFrame(bid_prices, columns=['Bid Price'])

# 绘制价格数据的分布图
plt.figure(figsize=(10, 6))
sns.histplot(bid_prices_df['Bid Price'], kde=True, bins=30)
plt.title('bid')
plt.xlabel('price')
plt.ylabel('frequency')
plt.show()
