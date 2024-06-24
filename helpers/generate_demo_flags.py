import numpy as np
from config import demo_flags

# Function to generate Demographics flags
def generate_demo_flags(df):
    for flag in demo_flags.keys():
        df[flag] = np.nan

    df['Flag_Demo_High_HHSize'] = (df['Sum_M_F'] > 30).astype(int)

    df['Flag_Demo_Inconsistent_HHSize'] = (df['Sum_M_F'] != df['HHSize']).astype(int)
    
    df['Flag_Demo_No_Adults'] = (df['Sum_adults'] == 0).astype(int)
    
    df['Flag_Demo_plw'] = (df['HHPregLactNb'] > df['in_plw_range']).astype(int)

    return df