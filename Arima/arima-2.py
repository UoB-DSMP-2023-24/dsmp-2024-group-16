
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

file_path = r'D:\TB2\mini-project\Tape.csv'
data = pd.read_csv(file_path)

data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d')
data.set_index('Date', inplace=True)

close_ts = data['Close']



#  chosen (1,1,1) which implies differencing once
# Define the model
model = ARIMA(data['Close'], order=(1,1,1))

# Fit the model
model_fit = model.fit()

# Make forecast
forecast = model_fit.forecast(steps=15)  # Forecasting the next 15 days

forecast



