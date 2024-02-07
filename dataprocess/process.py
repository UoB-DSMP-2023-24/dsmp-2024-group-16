import pandas as pd
import os

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

# Load and process the data
directory_path = 'C:/Users/Wilson/Desktop/TB2/Dataminiproject/Dataset'
combined_data = load_and_combine_datasets(directory_path)
daily_data = process_data(combined_data)

# Save the processed data to a CSV file
output_file_path = 'C:/Users/Wilson/Desktop/TB2/Dataminiproject/ProcessedData.csv'
daily_data.to_csv(output_file_path, index=False)
