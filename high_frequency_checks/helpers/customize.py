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
