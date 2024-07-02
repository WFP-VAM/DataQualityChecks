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
from high_frequency_checks.helpers.dataframe_customizer import DataFrameCustomizer
from high_frequency_checks.helpers.get_data import read_data
from high_frequency_checks.helpers.logging_config import LoggingHandler
from db_config import db_config

from data_bridges_knots import DataBridgesShapes



def main():
    pass


if __name__ == "__main__":
    CONFIG_PATH = r"data_bridges_api_config.yaml"

    # Set up Logging
    logging_handler = LoggingHandler()
    logger = logging_handler.logger
    error_handler = logging_handler.error_handler

    # Read configurations for base indicator
    config_handler = ConfigHandler()
    indicators = config_handler.get_indicators()
    base_cols, review_cols = config_handler.get_base_config()

    reports_folder = './reports'
    os.makedirs(reports_folder, exist_ok=True)
    report_all_indicators_path = os.path.join(reports_folder, f'{db_config["CountryName"]}_HFC_All_Indicators_Report.xlsx')
    report_mastersheet_path = os.path.join(reports_folder, f'{db_config["CountryName"]}_HFC_MasterSheet_Report.xlsx')

    # Generate All Indicators Report
    with pd.ExcelWriter(report_all_indicators_path) as writer:
        current_df = read_data(survey_id=db_config['DataBridgesIDs']['dataset'], config_path=CONFIG_PATH)
        # Specifically for DRC
        df_customizer = DataFrameCustomizer(current_df)
        current_df = df_customizer.rename_columns()
        current_df = df_customizer.create_urban_rural()
        
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
    