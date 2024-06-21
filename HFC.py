import pandas as pd
import numpy as np

# Read from dummy data (replace with your actual data loading)
df = pd.read_csv('congo.csv')

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

# Define FCS flags
fcs_flags = {
    'Flag_FCS_Missing_Values': 
        "One or more values in the FCS Module are missing!",
    'Flag_FCS_Erroneous_Values': 
        "One or more values in the FCS Module have Erroneous values (<0 or >7)",
    'Flag_FCS_Abnormal_Zeroes': 
        "All values in the FCS food groups are filled with 1's",
    'Flag_FCS_Abnormal_Sevens': 
        "All values in the FCS food groups are filled with 7's",
    'Flag_FCS_Abnormal_Identical': 
        "All values in the FCS food groups have the same value",
    'Flag_FCS_Low_Staple': 
        "Low Staple (Below 4)",
    'Flag_FCS_Low_FCS': 
        "Low FCS (10 or Below)",
    'Flag_FCS_High_FCS': 
        "High FCS (90 or Above)"
}

# Initialize flags
for flag in fcs_flags.keys():
    df[flag] = np.nan

# 1. Flag_FCS_Missing_Values: 1 if any column in FCS columns has missing values
df['Flag_FCS_Missing_Values'] = df[fcs_cols].isnull().any(axis=1).astype(int)

# 2. Flag_FCS_Erroneous_Values: 1 if any value in FCS columns is < 0 or > 7, but only if Flag_FCS_Missing_Values is 0
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
       'Flag_FCS_Low_Staple'] = low_staple_condition.astype(int)

# 7. Flag_FCS_Low_FCS: 1 if the value in FCS is 10 or Below, but only flag if Flag_FCS_Abnormal_Sevens is 0
low_fcs_condition = df['FCS'] <= 10
df.loc[df['Flag_FCS_Abnormal_Sevens'] == 0, 
       'Flag_FCS_Low_FCS'] = low_fcs_condition.astype(int)

# 8. Flag_FCS_High_FCS: 1 if the value in FCS is 90 or Above, but only flag if Flag_FCS_Abnormal_Sevens is 0
high_fcs_condition = df['FCS'] >= 90
df.loc[df['Flag_FCS_Abnormal_Sevens'] == 0, 
       'Flag_FCS_High_FCS'] = high_fcs_condition.astype(int)

# Set Flag_FCS to 1 if any of the columns in fcs_flag_columns have the value 1, else 0
df['Flag_FCS'] = (df[list(fcs_flags.keys())] == 1).any(axis=1).astype(int)

# Build narrative based on flags
df['Flag_FCS_Narrative'] = df[fcs_flags.keys()].apply(lambda row: " & ".join([fcs_flags[flag] for flag in fcs_flags if row[flag] == 1]), axis=1)

# Summarize flags for each household
hh_summary = df[['EnuName', 'FCSStap', 'FCSPulse', 'FCSDairy', 'FCSPr', 'FCSVeg', 'FCSFruit', 'FCSFat', 'FCSSugar', 'Flag_FCS_Missing_Values',
            'Flag_FCS_Erroneous_Values', 'Flag_FCS_Abnormal_Zeroes', 'Flag_FCS_Abnormal_Sevens', 'Flag_FCS_Abnormal_Identical',
            'Flag_FCS_Low_Staple', 'Flag_FCS_Low_FCS', 'Flag_FCS_High_FCS', 'Flag_FCS', 'Flag_FCS_Narrative']]

# Summarize flags for each enumerator with Total_Records and Error_Percentage
enu_summary = df.groupby('EnuName').agg({
    **{key: 'sum' for key in fcs_flags},  # Sum of all flag columns
    'EnuName': 'size',  # Total records per enumerator
    'Flag_FCS': 'sum'  # Sum of Flag_FCS
}).rename(columns={'EnuName': 'Total_Records'}).reset_index()

# Calculate Error Percentage
enu_summary['Error_Percentage'] = (enu_summary['Flag_FCS'] / enu_summary['Total_Records'])

# Summarize flags for each ID02 and EnuName with Total_Records and Error_Percentage
id02_enu_summary = df.groupby(['ID02', 'EnuName']).agg({
    **{key: 'sum' for key in fcs_flags},  # Sum of all flag columns
    'EnuName': 'size',  # Total records per enumerator
    'Flag_FCS': 'sum'  # Sum of Flag_FCS
}).rename(columns={'EnuName': 'Total_Records'}).reset_index()

# Calculate Error Percentage
id02_enu_summary['Error_Percentage'] = (id02_enu_summary['Flag_FCS'] / id02_enu_summary['Total_Records'])

# Write to Excel with two sheets: HH_Report and Enu_Report
with pd.ExcelWriter('HFC_Report.xlsx') as writer:
    hh_summary.to_excel(writer, sheet_name='HH_Report', index=False)
    enu_summary.to_excel(writer, sheet_name='Enu_Report', index=False)
    id02_enu_summary.to_excel(writer, sheet_name='Admin2_Enu_Report', index=False)


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
