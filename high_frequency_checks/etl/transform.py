import pandas as pd


def map_admin_areas(df):
    admin_areas = {
        'ID01': 'ADMIN1Name',
        'ID02': 'ADMIN2Name',
        'ID03': 'ADMIN3Name',
        'ID04LABEL': 'ADMIN4Name',
        'ID05': 'ADMIN5Name',
    }
    try:
        df = df.rename(columns=admin_areas)
    except KeyError:
        pass

    return df

def create_urban_rural(df):
    """
    Creates 2 columns in the DataFrame "Urban" and "Rural".
    
    Returns:
    pd.DataFrame: The DataFrame with new columns "Urban" and "Rural".
    """
    try:
        df['Urban'] = df['ID06'].apply(lambda x: '1' if x == '1' else '0')
        
        df['Rural'] = df['ID06'].apply(lambda x: '1' if x == '2' else '0')
    except KeyError:
        pass
    
    return df

def subset_for_enumerator_performance(data: pd.DataFrame) -> pd.DataFrame:
    """
    Subset the data for enumerator performance analysis.

    Args:
        data (pd.DataFrame): The input data.

    Returns:
        pd.DataFrame: A subset of the input data relevant for enumerator performance analysis.

    ## Enumerators checks

    - uuid
    - EnuName
    - Admin1/Admin2/Admin3
    - Labels for admin areas
    - condition for completed
    - Quota by Admin 2
    - GPS
    """
    
    
    try:
        data = data.rename(columns={'ID00': 'ADMIN0Name', "ID01": "ADMIN1Name", "ID02": "ADMIN2Name", "ID03": "ADMIN3Name", "ID04LABEL": "ADMIN4Name"})
    except KeyError:
        pass
    
    cols = ["_uuid", "start", "today", 'ADMIN0Name', 'ADMIN1Name', 'ADMIN2Name', "GPS", "EnuName", "EnuSupervisorName", "ADMIN4Name"]
    
    return data[cols]



def create_all_indicators_for_db(excel_file):
    # Read all sheets into a dictionary of DataFrames
    dfs = pd.read_excel(excel_file, sheet_name=None)

    # Create a list to store the modified DataFrames
    dfs_with_sheet_name = []

    # Iterate over the dictionary of DataFrames
    for sheet_name, df in dfs.items():
        # Add a column with the sheet name
        df['sheet_name'] = sheet_name
        
        dfs_with_sheet_name.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs_with_sheet_name, ignore_index=True)

    cols = ['_uuid', 'EnuName', 'EnuSupervisorName', 'ADMIN1Name', 'ADMIN2Name', 'ADMIN3Name', 'ADMIN4Name', 'today', 'Flag_Timing_Invalid_Duration', 'Flag_Timing_Short_Duration', 'Flag_Timing_Long_Duration', 'Flag_Timing_Abnormal_Start_Period', 'Flag_Timing_Overall', 'Flag_Timing_Narrative', 'Flag_Demo_Erroneous', 'Flag_Demo_High_HHSize', 'Flag_Demo_Inconsistent_HHSize', 'Flag_Demo_Missing', 'Flag_Demo_Narrative', 'Flag_Demo_No_Adults', 'Flag_Demo_Overall', 'Flag_Demo_PLW_Higher_F1259', 'Flag_FCS_Erroneous', 'Flag_FCS_High_FCS', 'Flag_FCS_Identical', 'Flag_FCS_Low_FCS', 'Flag_FCS_Low_Staple', 'Flag_FCS_Missing', 'Flag_FCS_Narrative', 'Flag_FCS_Overall', 'Flag_HHEXPF_7D_Erroneous', 'Flag_HHEXPF_7D_Missing', 'Flag_HHEXPF_7D_Narrative', 'Flag_HHEXPF_7D_Overall', 'Flag_HHEXPF_7D_Zero_FEXP', 'Flag_HHEXPNF_1M_Erroneous', 'Flag_HHEXPNF_1M_Missing', 'Flag_HHEXPNF_1M_Narrative', 'Flag_HHEXPNF_1M_Overall', 'Flag_HHEXPNF_6M_Erroneous', 'Flag_HHEXPNF_6M_Missing', 'Flag_HHEXPNF_6M_Narrative', 'Flag_HHEXPNF_6M_Overall', 'Flag_Housing_Displaced_Owner', 'Flag_Housing_Erroneous', 'Flag_Housing_Missing', 'Flag_Housing_Narrative', 'Flag_Housing_Overall', 'Flag_LCS_FS_Erroneous', 'Flag_LCS_FS_Missing', 'Flag_LCS_FS_Narrative', 'Flag_LCS_FS_No_Children', 'Flag_LCS_FS_NonExhaustive_Strategies_NA', 'Flag_LCS_FS_Overall', 'Flag_LCS_FS_R_Erroneous', 'Flag_LCS_FS_R_Missing', 'Flag_LCS_FS_R_Narrative', 'Flag_LCS_FS_R_No_Children', 'Flag_LCS_FS_R_NonExhaustive_Strategies_NA', 'Flag_LCS_FS_R_Overall', 'Flag_LCS_FS_R_Three_or_More_NA', 'Flag_LCS_FS_Three_or_More_NA', 'Flag_Timing_Abnormal_Start_Period', 'Flag_Timing_Invalid_Duration', 'Flag_Timing_Long_Duration', 'Flag_Timing_Narrative', 'Flag_Timing_Overall', 'Flag_Timing_Short_Duration', 'Flag_rCSI_Acceptable_FCG_High_Coping', 'Flag_rCSI_Erroneous', 'Flag_rCSI_Identical', 'Flag_rCSI_MealAdult_No_Children', 'Flag_rCSI_Missing', 'Flag_rCSI_Narrative', 'Flag_rCSI_Overall', 'Flag_rCSI_Poor_FCG_No_Coping', 'sheet_name']


    cols = ['_uuid', 'EnuName', 'EnuSupervisorName', 'ADMIN1Name', 'ADMIN2Name', 'ADMIN3Name', 'ADMIN4Name', 'today', 'sheet_name']
    
    combined_df = combined_df.rename(columns={'sheet_name': 'indicator', 'today': 'date'})
    

    # Print the combined DataFrame
    return combined_df
