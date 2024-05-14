import pandas as pd
import ast

# Load the data from CSV
df = pd.read_csv('lobs_par/UoB_Set01_2025-01-02LOBs.csv')

# Function to parse the list and extract the first element of the first array if available
def extract_first_element(lst_str):
    # Convert the string representation of list to actual list
    lst = ast.literal_eval(lst_str)
    # Check if the list is not empty and if the first array has at least one element
    if lst and lst[0]:
        # Return the first element of the first array
        return lst[0][0]
    return None

# Apply the function to 'Bid' and 'Ask' columns
df['Bid_first_element'] = df['Bid'].apply(extract_first_element)
df['Ask_first_element'] = df['Ask'].apply(extract_first_element)

# Display the first few rows of the modified dataframe to verify the changes
print(df[['Timestamp', 'Bid_first_element', 'Ask_first_element']].head())

# Save the modified dataframe back to CSV if needed
df.to_csv('mod_lob/01-02.csv', index=False)
