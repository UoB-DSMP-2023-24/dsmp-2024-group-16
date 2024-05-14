import ast
import pandas as pd
import matplotlib.pyplot as plt

# 读取特定日期的CSV文件
file_path = 'lobs_par/UoB_Set01_2025-01-02LOBs.csv'
data = pd.read_csv(file_path)

# 选择一个特定的时间点
specific_time_point = data.loc[9000]

# 提取买单和卖单信息
bids = ast.literal_eval(specific_time_point['Bid']) if specific_time_point['Bid'] else []
asks = ast.literal_eval(specific_time_point['Ask']) if specific_time_point['Ask'] else []

# 转换为DataFrame以便于操作
df_bids = pd.DataFrame(bids, columns=['Price', 'Quantity'])
df_asks = pd.DataFrame(asks, columns=['Price', 'Quantity'])

# 对买单按价格降序排序，卖单按价格升序排序
df_bids = df_bids.sort_values(by='Price', ascending=False)
df_asks = df_asks.sort_values(by='Price', ascending=True)

# 计算累积数量
df_bids['Cumulative Quantity'] = df_bids['Quantity'].cumsum()
df_asks['Cumulative Quantity'] = df_asks['Quantity'].cumsum()

# 绘制订单深度图
plt.figure(figsize=(10, 6))
plt.plot(df_bids['Price'], df_bids['Cumulative Quantity'], label='Bids', color='green')
plt.plot(df_asks['Price'], df_asks['Cumulative Quantity'], label='Asks', color='red')
plt.title('Order Book Depth at Specific Time Point')
plt.xlabel('Price')
plt.ylabel('Cumulative Quantity')
plt.legend()
plt.show()
