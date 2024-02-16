import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def load_and_combine_datasets(directory_path):
    combined_data = pd.DataFrame()
    for file_name in os.listdir(directory_path):
        if file_name.endswith('tapes.csv'):
            date_str = file_name.split('_')[2]
            date_str = date_str.rstrip('tapes.csv')
            try:
                date = pd.to_datetime(date_str)
            except ValueError as e:
                print(f"Error parsing date from file {file_name}: {e}")
                continue
            temp_data = pd.read_csv(os.path.join(directory_path, file_name), header=None, names=['Timestamp', 'Price', 'Volume'])
            temp_data['Date'] = date
            combined_data = pd.concat([combined_data, temp_data], ignore_index=True)
    return combined_data

def process_data(combined_data):
    daily_data = combined_data.groupby('Date').agg(
        Open=('Price', 'first'),
        High=('Price', 'max'),
        Low=('Price', 'min'),
        Close=('Price', 'last'),
        Volume=('Volume', 'sum')
    ).reset_index()
    return daily_data


directory_path = 'C:/Users/Wilson/Desktop/TB2/Dataminiproject/Dataset'
combined_data = load_and_combine_datasets(directory_path)
daily_data = process_data(combined_data)

# Prepare data for plotting
dates = mdates.date2num(daily_data['Date'])

# Assuming 'dates' is a list of datetime objects and 'daily_data' is a dictionary containing 'Open', 'High', 'Low', 'Close', and 'Volume' data.
fig, ax1 = plt.subplots(figsize=(10, 6))

# Set the x-axis as date.
ax1.set_xlabel('Date')

# Set the primary y-axis label for price.
ax1.set_ylabel('Price', color='black')  # Use black for the price axis label for clarity.

# Plot Open, High, Low, and Close prices.
ax1.plot_date(dates, daily_data['Open'], '-', label='Open', color='tab:green')
ax1.plot_date(dates, daily_data['High'], '-', label='High', color='tab:red')
ax1.plot_date(dates, daily_data['Low'], '-', label='Low', color='tab:blue')
ax1.plot_date(dates, daily_data['Close'], '-', label='Close', color='tab:gray')

# Set the date formatting for the x-axis.
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

# Create a secondary y-axis for Volume.
ax2 = ax1.twinx()
ax2.set_ylabel('Volume', color='tab:purple')  # Set the secondary y-axis label for volume.
ax2.plot_date(dates, daily_data['Volume'], '-', label='Volume', color='tab:purple')

# Add a title and legend.
plt.title('Stock Price and Volume')
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))

# Use tight layout to fit everything neatly.
plt.tight_layout()

# Display the plot.
plt.show()
