import numpy as np
import pandas as pd
from arch import arch_model
from arch.univariate import GARCH

# Load your data
data = pd.read_csv('Tapes\Tape.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)
data['log_return'] = np.log(data['Close'] / data['Close'].shift(1))
data.dropna(inplace=True)  # Ensure there are no NaN values in the data

# Define the GARCH model
model = arch_model(data['log_return'], mean='Constant', vol='Garch', p=1, q=1, dist='normal')
model.volatility = GARCH(p=1, q=1, power=2.0, o=0, constraints={'a[1] + b[1]': 1})

# Fit the model
res = model.fit(update_freq=5, disp='off')

# Print the summary of the model fit
print(res.summary())

# Forecast future volatility for 30 days
forecasts = res.forecast(horizon=30, method='simulation')

# Print the forecasted variance
print(forecasts.variance.iloc[-1])
