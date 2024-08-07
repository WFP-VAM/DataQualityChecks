
import os
import pandas as pd

def convert_to_pickle(data_folder='data'):
    for filename in os.listdir(data_folder):
        if filename.endswith(('.xlsx', '.csv')):
            file_path = os.path.join(data_folder, filename)
            file_name, file_extension = os.path.splitext(filename)
            
            if file_extension == '.xlsx':
                df = pd.read_excel(file_path)
            elif file_extension == '.csv':
                df = pd.read_csv(file_path)
            
            pickle_path = os.path.join(data_folder, f"{file_name}.pkl")
            df.to_pickle(pickle_path)
            print(f"Converted {filename} to {file_name}.pkl")
