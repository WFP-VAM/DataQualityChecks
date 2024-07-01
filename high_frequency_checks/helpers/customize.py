def rename_columns(df):
    """
    Renames columns in the DataFrame according to the given mapping.
    
    Parameters:
    df (pd.DataFrame): The DataFrame whose columns need to be renamed.
    column_mapping (dict): A dictionary where keys are current column names and values are the new column names.
    
    Returns:
    pd.DataFrame: The DataFrame with renamed columns.
    """
    
    column_mapping = {
        'ID01': 'ADMIN1Name',
        'ID02': 'ADMIN2Name',
        'ID03': 'ADMIN3Name',
        'ID04LABEL': 'ADMIN4Name',
        'ID05': 'ADMIN5Name',
    }
    
    df = df.rename(columns=column_mapping)
    return df

def create_urban_rural(df):
    """
    Creates 2 columns in the DataFrame "Urban" and "Rural".
    
    Parameters:
    df (pd.DataFrame): The DataFrame.
    
    Returns:
    pd.DataFrame: The DataFrame with renamed columns.
    """
    df['Urban'] = df['ID06'].apply(lambda x: '1' if x == '1' else '0')
    df['Rural'] = df['ID06'].apply(lambda x: '1' if x == '2' else '0')
    
    # Optionally, you can drop the original ID06 column if needed
    # df.drop('ID06', axis=1, inplace=True)
    
    return df