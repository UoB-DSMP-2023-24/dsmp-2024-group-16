import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime
import matplotlib.pyplot as plt

data = pd.read_csv('C:/Users/Wilson/Desktop/TB2/Dataminiproject/Tape.csv')

data.head(), data.tail()



data['Date'] = pd.to_datetime(data['Date'])


training_set = data[(data['Date'] >= '2025-01-01') & (data['Date'] <= '2025-05-31')]
test_set = data[(data['Date'] >= '2025-06-01') & (data['Date'] <= '2025-07-31')]


training_close_prices = training_set['Close']


model = ARIMA(training_close_prices, order=(1, 1, 1))
model_fit = model.fit()


forecast_steps = len(test_set)
forecast = model_fit.forecast(steps=forecast_steps)

forecast_dates = test_set['Date']
forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecast': forecast.values})


plt.figure(figsize=(16, 8))

plt.plot(data['Date'], data['Close'], label='Actual', color='blue')


plt.plot(training_set['Date'], training_set['Close'], label='Training Actual', color='green')


plt.plot(forecast_df['Date'], forecast_df['Forecast'], label='Forecast', color='red', linestyle='--')

plt.title('Actual vs Forecasted Close Prices (Jan to Jul)')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

