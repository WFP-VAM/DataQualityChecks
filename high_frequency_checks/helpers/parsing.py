import pandas as pd

def as_numeric(df, col_list):

    for col in col_list:
        try:
            df[col] = pd.to_numeric(df[col], errors='ignore').fillna(9999).astype('int64')
        except ValueError:
            continue
    
    return df
