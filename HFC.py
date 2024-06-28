import pandas as pd
from high_frequency_checks import Demo, Housing, FCS, rCSI, LCS, HDDS, FEXP_7D, NFEXP_1M, NFEXP_6M, MasterSheet
from config import config
from data_bridges_knots import DataBridgesShapes


CONFIG_PATH = r"data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

# Get data
def read_data(testing = False):
    if testing == True:
        print("Read data from local file")
        return pd.read_csv('data/congo.csv')
    else:
        print("Read data from DataBridges")
        df =  client.get_household_survey(survey_id=config["DataBridgesIDs"]['dataset'], access_type='full', page_size=800)
        print(f"Retrieved data for dataset #{config["DataBridgesIDs"]['dataset']}")
        print("\n --------------------------------------------------------- \n")
        return df

# List of Indicator Classes
indicators = [
    (Demo, 'Demo'),
    (Housing, 'Housing'),
    (FCS, 'FCS'),
    (rCSI, 'rCSI'),
    (LCS, 'LCS'),
    # (HDDS, 'HDDS'),
    (FEXP_7D, 'FEXP_7D'),
    (NFEXP_1M, 'NFEXP_1M'),
    (NFEXP_6M, 'NFEXP_6M')
]

def process_indicator(instance, writer):
    """Process the indicator instance."""
    instance.calculate_indicators()
    instance.generate_flags()
    instance.generate_report(writer)

if __name__ == "__main__":
    df = read_data(testing=False)
    output_dir = './reports'
    report_all_indicators_path = f'{output_dir}/HFC_All_Indicators_Report.xlsx'
    report_mastersheet_path = f'{output_dir}/HFC_MasterSheet_Report.xlsx'

    # Generate All Indicators Report
    with pd.ExcelWriter(report_all_indicators_path) as writer:
        current_df = df.copy()
        for indicator_class, config_key in indicators:
            config_values = config[config_key]
            instance = indicator_class(current_df, **config_values)
            process_indicator(instance, writer)
            current_df = instance.df.copy()

    # Generate MasterSheet Report
    mastersheet = MasterSheet(current_df)
    new_mastersheet_df = mastersheet.generate_dataframe()

    final_mastersheet_df = MasterSheet.merge_with_existing_report(new_mastersheet_df, report_mastersheet_path)

    with pd.ExcelWriter(report_mastersheet_path) as writer:
        final_mastersheet_df.to_excel(writer, sheet_name='MasterSheet', index=False)
