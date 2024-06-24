from config import male_cols, female_cols, adult_cols

def calculate_hh_size(df):
    
    df['Sum_M'] = df[male_cols].sum(axis=1)
    
    df['Sum_F'] = df[female_cols].sum(axis=1)

    df['Sum_M_F'] = df['Sum_M'] + df['Sum_F']
    
    return df

def calculate_total_adults(df):
    
    df['Sum_adults'] = df[adult_cols].sum(axis=1)
    
    return df

def calculate_total_plw_range(df):
    
    df['in_plw_range'] = df['HHSize1217F'] + ['HHSize1859F']
    
    return df