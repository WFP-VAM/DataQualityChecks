import numpy as np
from config import fcs_flags, fcs_cols

# Function to generate FCS flags
def generate_fcs_flags(df, low_fcs, high_fcs):
    for flag in fcs_flags.keys():
        df[flag] = np.nan

    # Missing Values
    df['Flag_FCS_Missing_Values'] = df[fcs_cols].isnull().any(axis=1).astype(int)
    
    # Erroneous Values
    condition = (df[fcs_cols] < 0) | (df[fcs_cols] > 7)
    df.loc[df['Flag_FCS_Missing_Values'] == 0,
           'Flag_FCS_Erroneous_Values'] = condition.any(axis=1).astype(int)
    
    # Identical values in all FCS groups
    identical_condition = df[fcs_cols].nunique(axis=1) == 1
    df.loc[df['Flag_FCS_Erroneous_Values'] == 0, 'Flag_FCS_Abnormal_Identical'] = identical_condition.astype(int)
    
    # Low Staple Consumption
    low_staple_condition = df['FCSStap'] < 4
    df.loc[df['Flag_FCS_Erroneous_Values'] == 0, 'Flag_FCS_Low_Staple'] = low_staple_condition.astype(int)
    
    # Low Food Consumption Score
    low_fcs_condition = df['FCS'] < low_fcs
    df.loc[df['Flag_FCS_Erroneous_Values'] == 0, 'Flag_FCS_Low_FCS'] = low_fcs_condition.astype(int)
    
    # High Food Consumption Score
    high_fcs_condition = df['FCS'] > high_fcs
    df.loc[df['Flag_FCS_Erroneous_Values'] == 0, 'Flag_FCS_High_FCS'] = high_fcs_condition.astype(int)
    
    # Poor Food Consumption with no Coping
    fcg_rcsi_condition = (df['FCSCat28'] == 'Poor') & (df['rCSI'] == 0)
    df.loc[df['Flag_FCS_Erroneous_Values'] == 0, 'Flag_FCS_Poor_FCG_Zero_rCSI'] = fcg_rcsi_condition.astype(int)
    
    # OVerall FCS Flag
    df['Flag_FCS'] = (df[list(fcs_flags.keys())] == 1).any(axis=1).astype(int)
    
    # Overall FCS Flag - Narrative
    narrative_flags = list(fcs_flags.keys())[:-1]
    df['Flag_FCS_Narrative'] = df[narrative_flags].apply(lambda row: " & ".join([fcs_flags[flag] for flag in narrative_flags if row[flag] == 1]), axis=1)
    
    return df