import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv('C:/Users/Wilson/Desktop/TB2/Dataminiproject/Tape.csv')



# Convert the 'Date' column to datetime format for easier manipulation
data['Date'] = pd.to_datetime(data['Date'])

# Calculating daily price fluctuation (volatility) as the difference between High and Low prices
data['Volatility'] = data['High'] - data['Low']

# Ensure the Date column is used for plotting
data.set_index('Date', inplace=True)


# Plotting with x-axis as actual days but labeled by months
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Volatility'], label='Daily Volatility', color='purple')

# Formatting the x-axis to show months
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(30))  # Assuming roughly 30 days per month for spacing
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))  # Year-Month format

plt.title('Price Volatility Over Time')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend()
plt.xticks(rotation=45)  # Rotate labels to avoid overlap
plt.grid(True)
plt.show()


