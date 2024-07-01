"""
This is the main entry point for the high frequency checks (HFC) application. It sets up logging, reads configuration files, and generates a report containing all the HFC indicators.

The main steps are:
1. Set up logging with file and stream handlers.
2. Read base indicator configuration from a YAML file.
3. Read configurations for each HFC indicator from YAML files.
4. Get data from DataBridges or a local file (for testing).
5. Generate an Excel report containing all the HFC indicators.
6. Check if there were any errors during data processing and print the error count.
"""

import os
import pandas as pd
from high_frequency_checks import MasterSheet, ConfigHandler
from high_frequency_checks.helpers.customize import rename_columns, create_urban_rural
from data_bridges_knots import DataBridgesShapes
from logging_config import LoggingHandler
from db_config import db_config


CONFIG_PATH = r"data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

if __name__ == "__main__":
    # Set up Logging
    logging_handler = LoggingHandler()
    logger = logging_handler.logger
    error_handler = logging_handler.error_handler

    # Read configurations for base indicator
    config_handler = ConfigHandler()
    indicators = config_handler.get_indicators()
    base_cols, review_cols = config_handler.get_base_config()

    # Get data
    def read_data_from_local():
        print("Read data from local file")
        return pd.read_csv('data/congo.csv')

    def read_data_from_databridges(client, survey_id):
        print("Read data from DataBridges")
        df = client.get_household_survey(survey_id=survey_id, access_type='full', page_size=800)
        print(f"Retrieved data for dataset #{survey_id}")
        print("\n --------------------------------------------------------- \n")
        return df

    def read_data(testing=False):
        if testing:
            return read_data_from_local()
        else:
            return read_data_from_databridges(client, db_config["DataBridgesIDs"]['dataset'])

    output_dir = './reports'
    report_all_indicators_path = os.path.join(output_dir, 'HFC_All_Indicators_Report.xlsx')
    report_mastersheet_path = os.path.join(output_dir, 'HFC_MasterSheet_Report.xlsx')

    # Generate All Indicators Report
    with pd.ExcelWriter(report_all_indicators_path) as writer:
        current_df = read_data()
        # Specifically for DRC Since it is not standardized
        current_df = rename_columns(current_df)
        current_df = create_urban_rural(current_df)
        for indicator_class, config_file in indicators:
            standard_config, configurable_config = config_handler.get_indicator_config(config_file)
            instance = indicator_class(df=current_df, base_cols=base_cols, review_cols=review_cols, 
                                       standard_config=standard_config, configurable_config=configurable_config,
                                       flags=indicator_class.flags)
            instance.process(writer)
            current_df = instance.df.copy()

    # Generate MasterSheet Report
    mastersheet = MasterSheet(current_df, base_cols, review_cols)
    new_mastersheet_df = mastersheet.generate_dataframe()
    final_mastersheet_df = MasterSheet.merge_with_existing_report(new_mastersheet_df, report_mastersheet_path)
    with pd.ExcelWriter(report_mastersheet_path) as writer:
        final_mastersheet_df.to_excel(writer, sheet_name='MasterSheet', index=False)
        
    # Terminal: Print if there were any errors
    error_count = error_handler.error_count
    warning_count = error_handler.warning_count
    print(f"Data processing completed with {error_count} errors and {warning_count} warnings.")
    