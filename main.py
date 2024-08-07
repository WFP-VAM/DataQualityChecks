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
from datetime import datetime
from data_bridges_knots import DataBridgesShapes
from high_frequency_checks import MasterSheet, ConfigHandler
from high_frequency_checks.etl.transform import map_admin_areas, create_urban_rural, subset_for_enumerator_performance, create_all_indicators_for_db
from high_frequency_checks.etl.load import load_data
from high_frequency_checks.helpers.logging_config import LoggingHandler
from high_frequency_checks.analysis.quotas import generate_quotas_report
from data_bridges_config import DATA_BRIDGES_CONFIG

CREDENTIALS = DATA_BRIDGES_CONFIG["credentials_file_path"]
COUNTRY_NAME = DATA_BRIDGES_CONFIG["country_name"]
REPORT_FOLDER = "./reports"
ALL_INDICATOR_REPORT = f'{COUNTRY_NAME}_HFC_All_Indicators_Report.xlsx'
MASTERSHEET_REPORT = f'{COUNTRY_NAME}_HFC_MasterSheet_Report.xlsx'

def setup_logging():
    logging_handler = LoggingHandler()
    return logging_handler.logger, logging_handler.error_handler

def create_reports_folder(reports_folder = REPORT_FOLDER):
    os.makedirs(reports_folder, exist_ok=True)
    report_all_indicators_path = os.path.join(reports_folder, ALL_INDICATOR_REPORT)
    report_mastersheet_path = os.path.join(reports_folder, MASTERSHEET_REPORT)
    return report_all_indicators_path, report_mastersheet_path

def generate_all_indicators_report(df, indicators, base_cols, report_path):
    with pd.ExcelWriter(report_path) as writer:
        current_df = df.copy()
        config_handler = ConfigHandler()
        for indicator_class, config_file in indicators:
            standard_config, configurable_config = config_handler.get_indicator_config(config_file)
            instance = indicator_class(
                df=current_df, 
                base_cols=base_cols, 
                standard_config=standard_config, 
                configurable_config=configurable_config,
                flags=indicator_class.flags
            )
            instance.process(writer)
            current_df = instance.df.copy()
    return current_df

def generate_mastersheet_report(df, base_cols, report_path):
    """
    Generates a mastersheet report from the provided DataFrame, base columns, and review columns.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the data.
        base_cols (list): A list of base columns to include in the mastersheet.
        report_path (str): The file path for the generated mastersheet report.

    Returns:
        pandas.DataFrame: The merged mastersheet DataFrame.
    """
    mastersheet = MasterSheet(df, base_cols)
    new_mastersheet_df = mastersheet.generate_dataframe()
    return MasterSheet.merge_with_existing_report(new_mastersheet_df, report_path)

def read_data(is_pipeline_working=True):
    """
    Reads data from Data Bridges for a given survey ID.
    """
    if is_pipeline_working == True:
        # Setup API client
        client = DataBridgesShapes(CREDENTIALS)
        survey_id = DATA_BRIDGES_CONFIG['survey_id']
        print("Getting data from DataBridges")
        df = client.get_household_survey(survey_id=survey_id, access_type='full', page_size=1000)
        
    else: 
        print("Getting data from Moda file extract")
        df = pd.read_csv(DATA_BRIDGES_CONFIG['data_file_extract'], low_memory=False)

    print(f"Data loaded for {df.shape[0]} entries, performing checks on survey")
    return df
    
if __name__ == "__main__":

    # Time setup
    start_time = datetime.now()
    timestamp = start_time.strftime("%m/%d/%Y, %H:%M:%S")

    # Setup logging
    logging_handler = LoggingHandler()
    logger = logging_handler.logger
    error_handler = logging_handler.error_handler

    # Read configurations for base indicator
    config_handler = ConfigHandler()
    indicators = config_handler.get_indicators()
    base_cols = config_handler.get_base_config()

    # Read data
    df = read_data(is_pipeline_working=False)

    # Generate quotas report
    admin_columns = ["_uuid", "ID01", "ID02",  "ID03", "ID04LABEL"]
    
    survey_completion_report = generate_quotas_report(df, admin_columns)

    # DRC specific standardization / mapping
    df = map_admin_areas(df)
    df = create_urban_rural(df)

    # Generate enumerator subset
    enumerator_report = subset_for_enumerator_performance(df)

    # Generate report folders
    report_all_indicators_path, report_mastersheet_path = create_reports_folder()

    # # Generate All Indicators Report
    full_report = generate_all_indicators_report(df, indicators, base_cols, report_all_indicators_path)

    # Generate mastersheet
    mastersheet_report = generate_mastersheet_report(full_report, base_cols, report_mastersheet_path)
    # Export reports in Excel
    with pd.ExcelWriter(report_mastersheet_path) as writer:
        mastersheet_report.to_excel(writer, sheet_name='MasterSheet', index=False)

    all_indicator_report = create_all_indicators_for_db(report_mastersheet_path)

    # # # # Load data to database
    load_data(mastersheet_report, "DRCDataQualitySummaryReport")
    load_data(enumerator_report, "DRCDataQualityEnumeratorReport")
    load_data(survey_completion_report, "DRCDataQualityCompletionReport")
    load_data(all_indicator_report, "DRCDataQualityAllIndicatorsReport")

    # Terminal: Print if there were any errors
    error_count = error_handler.error_count
    warning_count = error_handler.warning_count
    end_time = datetime.now()
    print(f"Data processing completed with {error_count} errors and {warning_count} warnings.")
    print(f"Total time taken: {end_time - start_time}")