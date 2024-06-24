import pandas as pd

def calculate_survey_duration(df):
    """
    Calculate survey duration in hours from 'start' and 'end' columns.
    
    Parameters:
    - df (DataFrame): Input DataFrame containing 'start' and 'end' columns.
    
    Returns:
    - DataFrame: DataFrame with an additional column 'survey_duration' in hours.
    """
    # Convert 'start' and 'end' columns to datetime if they are not already
    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])
    
    # Calculate survey duration in hours
    df['survey_duration'] = (df['end'] - df['start']).dt.total_seconds() / 3600
    
    return df
