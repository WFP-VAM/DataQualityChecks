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




if __name__ == "__main__":
    excel_file = r'C:\Users\alessandra.gherardel\OneDrive - World Food Programme\Documents\02. Information Management\02.Scripts\high_frequency_checks\reports\DRC_HFC_All_Indicators_Report.xlsx'
    all_indicators = get_indicators(excel_file)