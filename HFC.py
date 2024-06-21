import pandas as pd
import numpy as np

# Read from dummy data
df = pd.read_excel('congo.xlsx')

# Calculate FCS and generate FCS Flags---------------------------------------------------------------#
fcs_cols = ['FCSStap', 'FCSPulse', 'FCSDairy', 'FCSPr', 'FCSVeg', 'FCSFruit', 'FCSFat', 'FCSSugar']
df['FCS'] = (df['FCSStap'] * 2 +
             df['FCSPulse'] * 3 +
             df['FCSDairy'] * 4 +
             df['FCSPr'] * 4 +
             df['FCSVeg'] +
             df['FCSFruit'] +            
             df['FCSFat'] * 0.5 +
             df['FCSSugar'] * 0.5)

# Create FCG groups based on 21/35 or 28/42 thresholds ------------------------#
low_sugar_thresholds = [0, 21.5, 35.5, float('inf')]
high_sugar_thresholds = [0, 28.5, 42.5, float('inf')]

df['FCSCat21'] = pd.cut(df['FCS'], bins=low_sugar_thresholds, labels=['Poor', 'Borderline', 'Acceptable'], right=False)
df['FCSCat28'] = pd.cut(df['FCS'], bins=high_sugar_thresholds, labels=['Poor', 'Borderline', 'Acceptable'], right=False)

# Initialize FCS flags as nan
fcs_flag_columns = [
    'Flag_FCS_Missing_Values',
    'Flag_FCS_Erroneous_Values',
    'Flag_FCS_Abnormal_Zeroes',
    'Flag_FCS_Abnormal_Sevens',
    'Flag_FCS_Abnormal_Identical',
    'Flag_FCS_Low_Staple',
    'Flag_FCS_Low_FCS',
    'Flag_FCS_High_FCS'
]

# Initialize flags
for flag in fcs_flag_columns:
    df[flag] = np.nan

# 1. Flag_FCS_Missing_Values: 1 if any column in FCS columns has missing values
df['Flag_FCS_Missing_Values'] = df[fcs_cols].isnull().any(axis=1).astype(int)

# 2.Flag_FCS_Erroneous_Values: 1 if any value in FCS columns is < 0 or > 7, but only if Flag_FCS_Missing_Values is 0
condition = (df[fcs_cols] < 0) | (df[fcs_cols] > 7)
df.loc[df['Flag_FCS_Missing_Values'] == 0,
       'Flag_FCS_Erroneous_Values'] = condition.any(axis=1).astype(int)

# 3. Flag_FCS_Abnormal_Zeroes: 1 if all values in FCS columns are 0, but only flag if Flag_FCS_Erroneous_Values is 0
zero_condition = (df[fcs_cols] == 0).all(axis=1)
df.loc[df['Flag_FCS_Erroneous_Values'] == 0,
       'Flag_FCS_Abnormal_Zeroes'] = zero_condition.astype(int)

# 4. Flag_FCS_Abnormal_Sevens: 1 if all values in FCS columns are 7, but only flag if Flag_FCS_Abnormal_Zeroes is 0
seven_condition = (df[fcs_cols] == 7).all(axis=1)
df.loc[df['Flag_FCS_Abnormal_Zeroes'] == 0,
       'Flag_FCS_Abnormal_Sevens'] = seven_condition.astype(int)

# 5. Flag_FCS_Abnormal_Identical: 1 if all values in FCS columns are identical, but only flag if Flag_FCS_Abnormal_Sevens is 0
identical_condition = df[fcs_cols].nunique(axis=1) == 1
df.loc[df['Flag_FCS_Abnormal_Sevens'] == 0,
       'Flag_FCS_Abnormal_Identical'] = identical_condition.astype(int)

# 6. Flag_FCS_Low_Staple: 1 if the value in FCSStap is Below 4, but only flag if Flag_FCS_Abnormal_Sevens is 0
low_staple_condition = df['FCSStap'] < 4
df.loc[df['Flag_FCS_Abnormal_Sevens'] == 0, 
       'Flag_FCS_Low_Staple'] = (low_staple_condition).astype(int)

# 7. Flag_FCS_Low_FCS: 1 if the value in FCS is 10 or Below, but only flag if Flag_FCS_Abnormal_Sevens is 0
low_fcs_condition = df['FCS'] <= 10
df.loc[df['Flag_FCS_Abnormal_Sevens'] == 0, 
       'Flag_FCS_Low_FCS'] = (low_fcs_condition).astype(int)

# 8. Flag_FCS_High_FCS: 1 if the value in FCS is 90 or Above, but only flag if Flag_FCS_Abnormal_Sevens is 0
high_fcs_condition = df['FCS'] >= 90
df.loc[df['Flag_FCS_Abnormal_Sevens'] == 0, 
       'Flag_FCS_High_FCS'] = (high_fcs_condition).astype(int)

# Overall FCS Flag (Set to True if any flag is not None, indicating it has been checked)
df['Flag_FCS'] = df[fcs_flag_columns].notna().any(axis=1).astype(int)

df

# Calculate rCSI --------------------------------------------------------------# 

df['rCSI'] = (df['rCSILessQlty'] + 
                (df['rCSIBorrow'] * 2) + 
                df['rCSIMealNb'] + 
                df['rCSIMealSize'] + 
                (df['rCSIMealAdult'] * 3))


# Calculate LCS --------------------------------------------------------------# 

# Assign variable labels using a dictionary
variable_labels = {
    'Lcs_stress_DomAsset': "Sold household assets/goods (radio, furniture, refrigerator, television, jewellery etc.) due to lack of food",
    'Lcs_stress_Saving': "Spent savings due to lack of food",
    'Lcs_stress_EatOut': "Sent household members to eat elsewhere/live with family or friends due to lack of food",
    'Lcs_stress_CrdtFood': "Purchased food/non-food on credit (incur debts) due to lack of food",
    'Lcs_crisis_ProdAssets': "Sold productive assets or means of transport (sewing machine, wheelbarrow, bicycle, car, etc.) due to lack of food",
    'Lcs_crisis_Health': "Reduced expenses on health (including drugs) due to lack of food",
    'Lcs_crisis_OutSchool': "Withdrew children from school due to lack of food",
    'Lcs_em_ResAsset': "Mortgaged/Sold house or land due to lack of food",
    'Lcs_em_Begged': "Begged and/or scavenged (asked strangers for money/food) due to lack of food",
    'Lcs_em_IllegalAct': "Engaged in illegal income activities (theft, prostitution) due to lack of food"
}

# Value labels
value_labels = {
    10: "No, because I did not need to",
    20: "No, because I already sold those assets or have engaged in this activity within the last 12 months and cannot continue to do it",
    30: "Yes",
    9999: "Not applicable (don’t have access to this strategy)"
}

def apply_value_labels(series):
    return series.map(value_labels).astype('category')

# Create variables to specify if the household used any of the strategies by severity
# Stress
df['stress_coping_FS'] = np.where(df[['Lcs_stress_DomAsset', 'Lcs_stress_Saving', 'Lcs_stress_EatOut', 'Lcs_stress_CrdtFood']].isin([20, 30]).any(axis=1), 1, 0)

# Crisis
df['crisis_coping_FS'] = np.where(df[['Lcs_crisis_ProdAssets', 'Lcs_crisis_Health', 'Lcs_crisis_OutSchool']].isin([20, 30]).any(axis=1), 1, 0)

# Emergency
df['emergency_coping_FS'] = np.where(df[['Lcs_em_ResAsset', 'Lcs_em_Begged', 'Lcs_em_IllegalAct']].isin([20, 30]).any(axis=1), 1, 0)

# Calculate Max_coping_behaviour
df['Max_coping_behaviourFS'] = np.select(
    [df['emergency_coping_FS'] == 1,
     df['crisis_coping_FS'] == 1,
     df['stress_coping_FS'] == 1],
    [4, 3, 2],
    default=1
)

# Value labels for Max_coping_behaviourFS
max_coping_behaviour_labels = {
    1: "HH not adopting coping strategies",
    2: "Stress coping strategies",
    3: "Crisis coping strategies",
    4: "Emergency coping strategies"
}

df['Max_coping_behaviourFS'] = df['Max_coping_behaviourFS'].map(max_coping_behaviour_labels).astype('category')
