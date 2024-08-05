# Get data
import pandas as pd
from data_bridges_knots import DataBridgesShapes

def read_test_data():
    print("Reading data from local file")
    return pd.read_csv('data/congo.csv')

def read_data_from_databridges(survey_id, config_path = None):
    print(f"Reading data from DataBridges for id: {survey_id}")

    client = DataBridgesShapes(config_path)

    df = client.get_household_survey(survey_id=survey_id, access_type='full', page_size=1000)
    print(f"Retrieved data for dataset with id: {survey_id}")
    print("\n --------------------------------------------------------- \n")
    return df

def read_data(testing=False, config_path=None, survey_id=None):
    if testing:
        return read_test_data()
    else:
        return read_data_from_databridges(survey_id=survey_id, config_path=config_path)




def get_indicators(excel_file):
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

if __name__ == "__main__":
    excel_file = r'C:\Users\alessandra.gherardel\OneDrive - World Food Programme\Documents\02. Information Management\02.Scripts\high_frequency_checks\reports\DRC_HFC_All_Indicators_Report.xlsx'
    all_indicators = get_indicators(excel_file)