import pandas as pd


def map_admin_areas(df):
    admin_areas = {
        'ID01': 'ADMIN1Name',
        'ID02': 'ADMIN2Name',
        'ID03': 'ADMIN3Name',
        'ID04LABEL': 'ADMIN4Name',
        'ID05': 'ADMIN5Name',
    }
    try:
        df = df.rename(columns=admin_areas)
    except KeyError:
        pass

    return df

def create_urban_rural(df):
    """
    Creates 2 columns in the DataFrame "Urban" and "Rural".
    
    Returns:
    pd.DataFrame: The DataFrame with new columns "Urban" and "Rural".
    """
    try:
        df['Urban'] = df['ID06'].apply(lambda x: '1' if x == '1' else '0')
        
        df['Rural'] = df['ID06'].apply(lambda x: '1' if x == '2' else '0')
    except KeyError:
        pass
    
    return df
