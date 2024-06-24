from config import fcs_cols, fcs_weights

# Function to calculate FCS based on predefined weights
def calculate_fcs(df):
    df['FCS'] = df[fcs_cols].multiply(fcs_weights).sum(axis=1)
    return df