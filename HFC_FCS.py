import pandas as pd
from helpers import calculate_fcs, calculate_fcg, calculate_rcsi, generate_fcs_flags, generate_hdds_flags

from datetime import date

date = date.today()

# Read from dummy data (replace with your actual data loading)
df = pd.read_csv('congo.csv')

# Call the functions to process the data
df = calculate_fcs(df)
df = calculate_fcg(df)
df = calculate_rcsi(df)
df = generate_fcs_flags(df)
df = generate_hdds_flags(df)

# Generate reports
hh_summary = df[['EnuName', 'FCSStap', 'FCSPulse', 'FCSDairy', 'FCSPr', 'FCSVeg',
                 'FCSFruit', 'FCSFat', 'FCSSugar', 'FCS', 'FCSCat21', 'FCSCat28', 'rCSI',
                 'Flag_FCS_Missing_Values', 'Flag_FCS_Erroneous_Values', 
                 'Flag_FCS_Abnormal_Identical', 'Flag_FCS_Low_Staple', 'Flag_FCS_Low_FCS',
                 'Flag_FCS_High_FCS', 'Flag_FCS_Poor_FCG_Zero_rCSI', 'Flag_FCS', 
                 'Flag_FCS_Narrative', 
                 'Flag_HHDSStap', 'Flag_HHDSPulse', 'Flag_HDDSDairy', 'Flag_HDDSPr', 'Flag_HDDSVeg', 'Flag_HDDSFruit', 'Flag_HDDSFat', 'Flag_HDDSSugar', 'Flag_HDDSSugar']]

plot_flags_count(df, list(fcs_flags.keys())[:-1], fcs_flags, 'Reports/Flags_Count.png')

enu_summary = summarize_flags(df, 'EnuName', fcs_flags)
enu_summary = enu_summary[enu_summary['Error_Percentage'] >= 0.1].sort_values(by='Error_Percentage', ascending=True)
plot_error_percentage(enu_summary[['EnuName', 'Error_Percentage']], 'Reports/Enumerator_Err_Pct.png')

admin2_enu_summary = summarize_flags(df, ['ID02', 'EnuName'], fcs_flags)

# Write to Excel
with pd.ExcelWriter(f'Reports/{today}_HFC_Report.xlsx') as writer:
    hh_summary.to_excel(writer, sheet_name='HH_Report', index=False)
    enu_summary.to_excel(writer, sheet_name='Enu_Report', index=False)
    admin2_enu_summary.to_excel(writer, sheet_name='Admin2_Enu_Report', index=False)
