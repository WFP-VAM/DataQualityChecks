import pandas as pd
from helpers.calculate_fcg import calculate_fcg
from helpers.calculate_fcs import calculate_fcs
from helpers.calculate_rcsi import calculate_rcsi
from helpers.generate_fcs_flags import generate_fcs_flags
from helpers.summarize_flags import summarize_flags
from helpers.plot_flags_count import plot_flags_count
from helpers.plot_error_percentage import plot_error_percentage
from helpers.config import fcs_flags

# Read from dummy data (replace with your actual data loading)
df = pd.read_csv('congo.csv')

# Calculate Food Consumption Score
calculate_fcs(df)

# Categorize FCS into FCG
# Parameter: "True" if The consumption of sugar and oil is usually high in the context, "False" if otherwise
calculate_fcg(df, high_sugar_oil_consumption = True)

# Calculate Reduced Coping Strategy Index
calculate_rcsi(df)

# Generate Data Quality Flags for FCS
# Parameters: 14 for Low FCS and 100 for High FCS (Adjust if needed)
generate_fcs_flags(df, low_fcs=14, high_fcs=100)

# Generate reports
hh_summary = df[['EnuName', 'FCSStap', 'FCSPulse', 'FCSDairy', 'FCSPr', 'FCSVeg',
                 'FCSFruit', 'FCSFat', 'FCSSugar', 'FCS', 'FCSCat21', 'FCSCat28', 'rCSI',
                 'Flag_FCS_Missing_Values', 'Flag_FCS_Erroneous_Values', 
                 'Flag_FCS_Abnormal_Identical', 'Flag_FCS_Low_Staple', 'Flag_FCS_Low_FCS',
                 'Flag_FCS_High_FCS', 'Flag_FCS_Poor_FCG_Zero_rCSI', 'Flag_FCS', 
                 'Flag_FCS_Narrative']]

plot_flags_count(df, list(fcs_flags.keys())[:-1], fcs_flags, 'Reports/Flags_Count.png')

enu_summary = summarize_flags(df, 'EnuName', fcs_flags)
enu_summary = enu_summary[enu_summary['Error_Percentage'] >= 0.1].sort_values(by='Error_Percentage', ascending=True)
plot_error_percentage(enu_summary[['EnuName', 'Error_Percentage']], 'Reports/Enumerator_Err_Pct.png')

id02_enu_summary = summarize_flags(df, ['ID02', 'EnuName'], fcs_flags)

# Write to Excel
with pd.ExcelWriter('Reports/HFC_Report.xlsx') as writer:
    hh_summary.to_excel(writer, sheet_name='HH_Report', index=False)
    enu_summary.to_excel(writer, sheet_name='Enu_Report', index=False)
    id02_enu_summary.to_excel(writer, sheet_name='Admin2_Enu_Report', index=False)
