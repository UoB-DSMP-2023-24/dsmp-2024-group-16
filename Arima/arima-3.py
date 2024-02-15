import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

file_path = r'D:\TB2\mini-project\Tape.csv'
data = pd.read_csv(file_path)

data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d')
data.set_index('Date', inplace=True)

# 平稳性检查
close_ts = data['Close']


# 计算用于训练和测试的分割点
split_point = int(len(close_ts) * 0.8)

# 分割数据为训练集和测试集
train, test = close_ts[:split_point], close_ts[split_point:]

# 使用训练数据拟合ARIMA模型
model_train = ARIMA(train, order=(2, 1, 2))
model_train_fit = model_train.fit()

# 使用拟合的模型对测试集进行预测
forecast_test = model_train_fit.forecast(steps=len(test))

# 绘制实际值和预测值以进行比较
plt.figure(figsize=(12, 6))
plt.plot(train.index, train, label='Train')
plt.plot(test.index, test, label='Actual Test')
plt.plot(test.index, forecast_test, label='Forecast Test', linestyle='--')
plt.title('Train, Test and Forecast using ARIMA Model')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.grid(True)
plt.show()