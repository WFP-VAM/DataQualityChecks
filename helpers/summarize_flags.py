# Function to summarize flags by a group (e.g., EnuName)
def summarize_flags(df, groupby_col, fcs_flags):
    enu_summary = df.groupby(groupby_col).agg({
        **{key: 'sum' for key in fcs_flags},
        'EnuName': 'size',
        'Flag_FCS': 'sum'
    }).rename(columns={'EnuName': 'Total_Records'}).reset_index()
    enu_summary['Error_Percentage'] = enu_summary['Flag_FCS'] / enu_summary['Total_Records']
    return enu_summary