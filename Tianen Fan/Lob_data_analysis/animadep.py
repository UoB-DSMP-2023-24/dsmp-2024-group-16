import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast
from matplotlib.animation import FuncAnimation

# 定义一个函数，用于从字符串表示的列表中解析订单
def parse_orders(orders_str):
    try:
        return ast.literal_eval(orders_str)
    except ValueError:
        return []

# 更新图表的函数
def update(frame_number, ax, data):
    ax.clear()
    current_time_point = data.iloc[frame_number]
    bids = parse_orders(current_time_point['Bid'])
    asks = parse_orders(current_time_point['Ask'])

    # 将买单和卖单转换为DataFrame
    df_bids = pd.DataFrame(bids, columns=['Price', 'Quantity']) if bids else pd.DataFrame(columns=['Price', 'Quantity'])
    df_asks = pd.DataFrame(asks, columns=['Price', 'Quantity']) if asks else pd.DataFrame(columns=['Price', 'Quantity'])

    # 计算累积数量
    df_bids = df_bids.sort_values(by='Price', ascending=False)
    df_asks = df_asks.sort_values(by='Price', ascending=True)
    df_bids['Cumulative Quantity'] = df_bids['Quantity'].cumsum()
    df_asks['Cumulative Quantity'] = df_asks['Quantity'].cumsum()

    # 绘制买单和卖单的累积曲线
    ax.plot(df_bids['Price'], df_bids['Cumulative Quantity'], color='green', label='Bids')
    ax.plot(df_asks['Price'], df_asks['Cumulative Quantity'], color='red', label='Asks')
    ax.set_title(f"Order Book Depth at Time {frame_number}")
    ax.set_xlabel('Price')
    ax.set_ylabel('Cumulative Quantity')
    ax.legend()

# 加载CSV文件
file_path = 'test.csv'  # 更改为您的文件路径
data = pd.read_csv(file_path)

# 初始化图表
fig, ax = plt.subplots()

# 创建动画
ani = FuncAnimation(fig, update, frames=np.arange(0, len(data), 10), fargs=(ax, data), repeat=False)

# 显示或保存动画
plt.show()
ani.save('order_book_depth_animation.gif', writer='pillow', fps=3)

