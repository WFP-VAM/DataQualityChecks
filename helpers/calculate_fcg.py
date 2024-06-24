import pandas as pd

# Function to categorize FCS into FCG groups
def calculate_fcg(df):
    def categorize_fcs(fcs, thresholds):
        return pd.cut(fcs, bins=thresholds, labels=['Poor', 'Borderline', 'Acceptable'], right=False)
    
    low_sugar_thresholds = [0, 21.5, 35.5, float('inf')]
    high_sugar_thresholds = [0, 28.5, 42.5, float('inf')]
    df['FCSCat21'] = categorize_fcs(df['FCS'], low_sugar_thresholds)
    df['FCSCat28'] = categorize_fcs(df['FCS'], high_sugar_thresholds)
    
    return df