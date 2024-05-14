import pandas as pd

# Load the CSV file 
file_path = r'D:\TB2\mini-project\Tape.csv'
data = pd.read_csv(file_path)

# Display 
data.head(), data.info(), data.describe()



from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

# 转换日期列为时间序列索引
data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d')
data.set_index('Date', inplace=True)

# 平稳性检查
close_ts = data['Close']

# 差分
close_diff = close_ts.diff().dropna()


# 使用ADF检验检查时间序列的平稳性
adf_result = adfuller(close_ts)

# 绘制'Close'时间序列图
plt.figure(figsize=(10, 6))
plt.plot(close_ts)
plt.title('Close Price Time Series')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.grid(True)
plt.show(), adf_result

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# 绘制ACF图和PACF图以帮助确定ARIMA模型的p和q参数
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

# ACF图
plot_acf(close_diff, ax=ax1, lags=20)
ax1.set_title('Autocorrelation Function')

# PACF图
plot_pacf(close_diff, ax=ax2, lags=20)
ax2.set_title('Partial Autocorrelation Function')

plt.show()
