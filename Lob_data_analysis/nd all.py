import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 文件夹路径，根据您的文件夹路径进行修改
folder_path = 'lobs_par'

# 存储每个文件的平均差值的绝对值
daily_avg_diffs = []

# 遍历文件夹中的每个文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv') or file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)
        # 读取数据
        data = pd.read_csv(file_path) if file_name.endswith('.csv') else pd.read_excel(file_path)

        # 提取Bid和Ask的第一个价格数据
        data['Bid Price'] = data['Bid'].apply(lambda x: eval(x)[0][0] if x != '[]' else np.nan)
        data['Ask Price'] = data['Ask'].apply(lambda x: eval(x)[0][0] if x != '[]' else np.nan)

        # 计算差值的绝对值
        data['Abs Diff'] = (data['Ask Price'] - data['Bid Price']).abs()

        # 计算当天的平均差值的绝对值
        daily_avg_diff = data['Abs Diff'].mean()

        # 添加到列表中
        daily_avg_diffs.append(daily_avg_diff)

# 移除NaN值
daily_avg_diffs = [x for x in daily_avg_diffs if pd.notnull(x)]

# 绘制正态分布图
sns.histplot(daily_avg_diffs, kde=True)
plt.title('Daily Avg Difference')
plt.xlabel('dif')
plt.ylabel('frequency')
plt.show()
