import numpy as np
from config import fcs_flags, fcs_cols

# Function to generate FCS flags
def generate_fcs_flags(df):
    for flag in fcs_flags.keys():
        df[flag] = np.nan

    df['Flag_FCS_Missing_Values'] = df[fcs_cols].isnull().any(axis=1).astype(int)
    condition = (df[fcs_cols] < 0) | (df[fcs_cols] > 7)
    df.loc[df['Flag_FCS_Missing_Values'] == 0, 'Flag_FCS_Erroneous_Values'] = condition.any(axis=1).astype(int)
    identical_condition = df[fcs_cols].nunique(axis=1) == 1
    df.loc[df['Flag_FCS_Erroneous_Values'] == 0, 'Flag_FCS_Abnormal_Identical'] = identical_condition.astype(int)
    low_staple_condition = df['FCSStap'] < 4
    df.loc[df['Flag_FCS_Erroneous_Values'] == 0, 'Flag_FCS_Low_Staple'] = low_staple_condition.astype(int)
    low_fcs_condition = df['FCS'] <= 10
    df.loc[df['Flag_FCS_Erroneous_Values'] == 0, 'Flag_FCS_Low_FCS'] = low_fcs_condition.astype(int)
    high_fcs_condition = df['FCS'] >= 90
    df.loc[df['Flag_FCS_Erroneous_Values'] == 0, 'Flag_FCS_High_FCS'] = high_fcs_condition.astype(int)
    fcg_rcsi_condition = (df['FCSCat28'] == 'Poor') & (df['rCSI'] == 0)
    df.loc[df['Flag_FCS_Erroneous_Values'] == 0, 'Flag_FCS_Poor_FCG_Zero_rCSI'] = fcg_rcsi_condition.astype(int)
    df['Flag_FCS'] = (df[list(fcs_flags.keys())] == 1).any(axis=1).astype(int)
    narrative_flags = list(fcs_flags.keys())[:-1]
    df['Flag_FCS_Narrative'] = df[narrative_flags].apply(lambda row: " & ".join([fcs_flags[flag] for flag in narrative_flags if row[flag] == 1]), axis=1)
    return df