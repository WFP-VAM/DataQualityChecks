"""
The main entry point of the application. This script is responsible for the following tasks:

1. Set up logging configuration.
2. Read indicator configurations from a YAML file.
3. Create necessary directories for report generation.
4. Generate an "All Indicators Report" in an Excel file.
5. Generate a "MasterSheet Report" in an Excel file.
6. Upload the MasterSheet report to a database.
7. Print the number of errors and warnings encountered during data processing.
"""

import os
import pandas as pd
from high_frequency_checks import MasterSheet, ConfigHandler, ConfigGenerator
from high_frequency_checks.helpers.dataframe_customizer import DataFrameCustomizer
from high_frequency_checks.etl.get_data import read_data, subset_for_enumerator_performance, get_indicators
from high_frequency_checks.etl.load_data import load_data
from high_frequency_checks.helpers.logging_config import LoggingHandler
from db_config import db_config

# Credentials for database and API
CREDENTIALS = r"databridges_api_database_credentials.yaml"

def main():
    # Set up Logging
    logging_handler = LoggingHandler()
    logger = logging_handler.logger
    error_handler = logging_handler.error_handler

    # Define the input directory and file path
    input_directory = "high_frequency_checks/config"  # Replace with your actual input directory path
    config_file_path = os.path.join(input_directory, 'config.csv')

    # Check if config.csv exists in the input directory
    if os.path.isfile(config_file_path):
        # Read configuration from MODA csv and generate config files
        config_generator = ConfigGenerator()
        config_generator.generate_configs()

    # Read configurations for base indicator
    config_handler = ConfigHandler()
    indicators = config_handler.get_indicators()
    base_cols, review_cols = config_handler.get_base_config()

    # report writing 
    reports_folder = './reports'
    os.makedirs(reports_folder, exist_ok=True)

    reports = {
        "all_indicators": f'{db_config["CountryName"]}_HFC_All_Indicators_Report.xlsx',
        "mastersheet": f'{db_config["CountryName"]}_HFC_MasterSheet_Report.xlsx'
    } 

    report_all_indicators_path = os.path.join(reports_folder, reports["all_indicators"])

    report_mastersheet_path = os.path.join(reports_folder, reports['mastersheet'])

    df = read_data(survey_id=db_config['DataBridgesIDs']['dataset'], config_path=CREDENTIALS)

    # Generate All Indicators Report
    with pd.ExcelWriter(report_all_indicators_path) as writer:
        current_df = df
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

    # Upload Mastersheet to database
    master_table_name = f"{db_config["CountryName"]}DataQualitySummaryReport"
    mastersheets_cols_to_drop = ["Flag_Narrative_Final", "Reviewed", "Review_Date", "Reviewed_By", "Action_Taken"]
    mastersheet_report = final_mastersheet_df.drop(columns=mastersheets_cols_to_drop)
    load_data(mastersheet_report, master_table_name)
    
    # Upload disaggregated report to database
    disaggregated_table_name = f"{db_config['CountryName']}DataQualityAllIndicatorsReport"
    excel_file = r'reports\DRC_HFC_All_Indicators_Report.xlsx'
    all_indicators = get_indicators(excel_file)
    load_data(all_indicators, disaggregated_table_name)

    # Process for Tableau and upload to abase    
    enumerator_df = subset_for_enumerator_performance(df)
    load_data(enumerator_df, f"{db_config["CountryName"]}DataQualityEnumeratorReport")

    # Terminal: Print if there were any errors
    error_count = error_handler.error_count
    warning_count = error_handler.warning_count
    print(f"Data processing completed with {error_count} errors and {warning_count} warnings.")
    
if __name__ == "__main__":
    main()
    

