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


fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel('Date')
ax.set_ylabel('Open Price', color='tab:green')
ax.plot_date(dates, daily_data['Open'], '-', label='Open', color='tab:green')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)
plt.title('Monthly Open Price Dynamics')
plt.legend()
plt.tight_layout()
plt.show()


fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel('Date')
ax.set_ylabel('High Price', color='tab:red')
ax.plot_date(dates, daily_data['High'], '-', label='High', color='tab:red')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)
plt.title('Monthly High Price Dynamics')
plt.legend()
plt.tight_layout()
plt.show()


fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel('Date')
ax.set_ylabel('Low Price', color='tab:blue')
ax.plot_date(dates, daily_data['Low'], '-', label='Low', color='tab:blue')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)
plt.title('Monthly Low Price Dynamics')
plt.legend()
plt.tight_layout()
plt.show()


fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel('Date')
ax.set_ylabel('Close Price', color='tab:gray')
ax.plot_date(dates, daily_data['Close'], '-', label='Close', color='tab:gray')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)
plt.title('Monthly Close Price Dynamics')
plt.legend()
plt.tight_layout()
plt.show()


fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel('Date')
ax.set_ylabel('Volume', color='tab:purple')
ax.plot_date(dates, daily_data['Volume'], '-', label='Volume', color='tab:purple')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)
plt.title('Monthly Volume Dynamics')
plt.legend()
plt.tight_layout()
plt.show()

