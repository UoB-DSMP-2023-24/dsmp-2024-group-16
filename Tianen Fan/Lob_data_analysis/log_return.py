import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 加载数据
file_path = 'Tapes/Tape.csv'
data = pd.read_csv(file_path)

# 将日期从字符串转换为datetime类型
data['Date'] = pd.to_datetime(data['Date'])

# 计算日对数收益率
data['Log_Return'] = np.log(data['Close'] / data['Close'].shift(1))

# 创建图形
plt.figure(figsize=(14,7))

# 绘制日对数收益率随时间变化的图
plt.plot(data['Date'], data['Log_Return'], marker='o', linestyle='-', color='blue')

# 设置图形的标题和坐标轴标签
plt.title('Daily Log Returns Over Time')
plt.xlabel('Date')
plt.ylabel('Log Return')

# 设置x轴主刻度为每月的第一天
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))

# 设置x轴刻度的显示格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))

# 只显示7个x轴的刻度点，从1月到7月
plt.xlim([data['Date'].min(), data['Date'].min() + pd.DateOffset(months=6)])

# 在y=0处添加水平辅助线
plt.axhline(y=0, color='red', linestyle='--')

# 自动旋转日期标记以提高可读性
plt.gcf().autofmt_xdate()

# 显示网格
plt.grid(True)

# 调整布局
plt.tight_layout()

# 显示图形
plt.show()
