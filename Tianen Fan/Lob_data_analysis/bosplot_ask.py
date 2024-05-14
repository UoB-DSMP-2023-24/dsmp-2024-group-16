import os
import pandas as pd
import matplotlib.pyplot as plt
import ast

# 定义函数以安全方式从字符串中提取价格信息
def extract_prices(data_column):
    prices = []
    for item in data_column:
        if item:  # 检查列表是否为空
            orders = ast.literal_eval(item)  # 安全地将字符串解析为列表
            prices.extend([price for price, _ in orders])
    return prices

# 文件夹路径
folder_path = 'lobs_par'

# 初始化字典来存储不同日期的价格
bid_prices_by_day = {}
ask_prices_by_day = {}

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    # 确保处理的是CSV文件
    if file_name.endswith('.csv'):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, file_name)
        # 读取CSV文件
        data = pd.read_csv(file_path)
        # 提取日期作为键，文件名示例：'UoB_Set01_2025-01-02LOBs.csv'
        date = file_name.split('_')[2]  # 根据实际文件名结构调整
        # 提取并存储价格数据
        bid_prices_by_day[date] = extract_prices(data['Bid'])
        ask_prices_by_day[date] = extract_prices(data['Ask'])

# 现在我们有了所有日期的价格数据，可以绘制箱线图
# 这里以买单价格为例
plt.figure(figsize=(20, 10))  # 根据需要调整尺寸
plt.boxplot(ask_prices_by_day.values(), labels=ask_prices_by_day.keys())
plt.title('ask Price Distribution Comparison Across Days')
plt.ylabel('Price')
plt.xticks(rotation=90)  # 旋转标签以适应
plt.show()
