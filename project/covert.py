import pandas as pd
import os

# Directory containing the .xlsb files
input_directory = '/Users/tai/Project/project'
output_directory = '/Users/tai/Project/project'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate through all files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.xlsb'):
        # Construct full file path
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, filename.replace('.xlsb', '.csv'))
        
        # Read the .xlsb file
        df = pd.read_excel(input_file_path, engine='pyxlsb')
        
        # Convert to .csv
        df.to_csv(output_file_path, index=False)