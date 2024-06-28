import pandas as pd
from data_bridges_knots import DataBridgesShapes

from high_frequency_checks import Demo, Housing, FCS, rCSI, LCS, HDDS, FEXP_7D, NFEXP_1M, NFEXP_6M, MasterSheet
from high_frequency_checks.helpers.load import load_data
from config import config
from datetime import datetime
import logging

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
    (HDDS, 'HDDS'),
    (FEXP_7D, 'FEXP_7D'),
    (NFEXP_1M, 'NFEXP_1M'),
    (NFEXP_6M, 'NFEXP_6M')
]

def process_indicator(instance, writer):
    """Process the indicator instance."""
    instance.calculate_indicators() # drops after this one.
    instance.generate_flags()
    instance.generate_report(writer)


def write_to_excel():
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
    print(f"Generated reports for {config['CountryName']} at {datetime.now()}")


if __name__ == "__main__":

    master_table_name = f"DQ_Mastersheet_{config["CountryName"]}"

    df = read_data(testing=False)
    output_dir = './reports'
    report_all_indicators_path = f'{output_dir}/{config["CountryName"]}_HFC_All_Indicators_Report.xlsx'
    report_mastersheet_path = f'{output_dir}/{config["CountryName"]}_HFC_MasterSheet_Report.xlsx'

    write_to_excel()

    # Upload to DataBase
    master_table_name = f"DQ_Mastersheet_{config["CountryName"]}"
    load_data(report_mastersheet_path, "MasterSheet", master_table_name)

