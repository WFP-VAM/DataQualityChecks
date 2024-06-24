import pandas as pd

# Function to categorize FCS into FCG groups
def calculate_fcg(df, high_sugar_oil_consumption):
    
    def categorize_fcs(fcs, thresholds):
        return pd.cut(fcs, bins=thresholds, labels=['Poor', 'Borderline', 'Acceptable'], right=False)
    
    if high_sugar_oil_consumption == True:
        thresholds = [0, 28.5, 42.5, float('inf')]
        df['FCSCat28'] = categorize_fcs(df['FCS'], thresholds)
        
    elif high_sugar_oil_consumption == False:
        thresholds = [0, 21.5, 35.5, float('inf')]
        df['FCSCat21'] = categorize_fcs(df['FCS'], thresholds)

    return df