import os
import re

# regular expression[x, y]，x>10 & x<500
pattern = r'\[([5-9]\d{2,}|[1-9]\d{3,}|[1-9])\s*,\s*\d+\]'

# Folder Path
input_folder_path = r'D:\TB2\mini-project\LOBs'
output_folder_path = r'D:\TB2\mini-project\LOBss' 

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Get all file names in a folder
file_names = os.listdir(input_folder_path)

# Iterate through each file in the folder
for file_name in file_names:
    if file_name.endswith('.txt'):
        # The full input path to the build file
        input_file_path = os.path.join(input_folder_path, file_name)

        # Open the file and read the contents
        with open(input_file_path, 'r') as file:
            text = file.read()

        # Replacing matched text with an empty string using regular expressions
        result = re.sub(pattern, '', text)

        # Build the full path to the output file
        output_file_path = os.path.join(output_folder_path, file_name)
        
        # Open a new txt file in write mode
        with open(output_file_path, 'w') as output_file:
            output_file.write(result)

print("success!")
