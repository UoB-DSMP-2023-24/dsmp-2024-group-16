import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Replace 'your_folder_path' with the actual path of the folder containing your CSV files
folder_path = 'lobs_par'

# Function to calculate the variance of the first ask prices in a file
def calculate_variance(file_path):
    data = pd.read_csv(file_path)
    # 确保每个条目是有效的数值字符串
    ask_prices = []
    for ask in data['Ask']:
        if ask.startswith('['):
            # 取出价格部分并确保它是有效的数字字符串
            try:
                price_str = ask.split(',')[0][2:]  # 提取价格字符串
                price = float(price_str)  # 尝试转换为浮点数
                ask_prices.append(price)
            except ValueError:
                # 如果转换失败（例如，空字符串或非数值字符串），则跳过这个条目
                continue
    return np.var(ask_prices)


# Get a list of all CSV files in the folder
file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

# Calculate the variance for each file and store the results with the corresponding date
variance_by_date = {}
for file_path in file_paths:
    # Extracting the month-date part from the filename
    month_day_str = os.path.basename(file_path).split('_')[2][5:10]  # '2025-01-02LOBs.csv' -> '01-02'
    variance_by_date[month_day_str] = calculate_variance(file_path)


sorted_dates = sorted(variance_by_date.keys(), key=lambda x: datetime.strptime(x, "%m-%d"))
sorted_variances = [variance_by_date[date] for date in sorted_dates]

# Plot the variance over time
plt.figure(figsize=(10, 5))
plt.plot(sorted_dates, sorted_variances, marker='o')
plt.xlabel('Date (Month-Day)')
plt.ylabel('Variance of First Ask Prices')
plt.title('Variance of First Ask Prices Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()