import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
folder_path = 'lobs_par_test'

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
        # 提取日期作为键，这里先去掉'LOBs.csv'然后再分割
        date_str = file_name.replace('LOBs.csv', '').split('_')[-1]
        date = pd.to_datetime(date_str)  # 转换字符串为datetime对象
        # 提取并存储价格数据
        bid_prices_by_day[date] = extract_prices(data['Bid'])
        ask_prices_by_day[date] = extract_prices(data['Ask'])


# 转换键为日期格式，以便matplotlib能够理解和格式化
dates = sorted(bid_prices_by_day.keys())
# Assuming the keys in bid_prices_by_day are already datetime objects:
dates = sorted(bid_prices_by_day.keys())



# 绘制箱线图
plt.figure(figsize=(20, 10))  # 根据需要调整尺寸

# 生成箱线图，使用已经排序和转换格式的日期作为标签
plt.boxplot([bid_prices_by_day[date] for date in dates], labels=[date.strftime('%Y-%m-%d') for date in dates])


# 设置图表的日期格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

# 这将自动旋转日期标签，以防它们重叠
plt.gcf().autofmt_xdate()

plt.title('Bid Price Distribution Comparison Across Days')
plt.ylabel('Price')
plt.show()
