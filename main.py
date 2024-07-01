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
import yaml
import logging
import pandas as pd
from datetime import datetime
from high_frequency_checks import Demo, Housing, FCS, rCSI, LCS_FS, LCS_FS_R, LCS_EN, HHEXPF_7D, HHEXPNF_1M, HHEXPNF_6M, MasterSheet
from high_frequency_checks.helpers.customize import rename_columns
from data_bridges_knots import DataBridgesShapes
import logging
from config import config

CONFIG_PATH = r"data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

class ErrorHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.error_count = 0

    def emit(self, record):
        if record.levelno >= logging.ERROR:
            self.error_count += 1

# Function to read YAML file
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

if __name__ == "__main__":
    # Set up logging directory and file
    log_folder = 'logs'
    os.makedirs(log_folder, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = os.path.join(log_folder, f'hfc_log_{timestamp}.log')

    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # File handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Stream handler for console output (errors only)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Create and add the error handler
    error_handler = ErrorHandler()
    logger.addHandler(error_handler)

    # Read configurations for base indicator
    base_config_path = os.path.join('high_frequency_checks', 'config', 'configurable', 'base_indicator.yaml')
    base_config = read_yaml(base_config_path)
    base_cols = list(base_config.get('base_cols', []))
    review_cols = list(base_config.get('review_cols', []))
    
    # Read configurations for indicators
    standard_config_dir = os.path.join('high_frequency_checks', 'config', 'standard')
    configurable_config_dir = os.path.join('high_frequency_checks', 'config', 'configurable')
    
    indicators = [
        (Demo, 'demo.yaml'),
        (Housing, 'housing.yaml'),
        (FCS, 'fcs.yaml'),
        (rCSI, 'rcsi.yaml'),
        (LCS_FS, 'lcs_fs.yaml'),
        (LCS_FS_R, 'lcs_fs_r.yaml'),
        (LCS_EN, 'lcs_en.yaml'),
        (HHEXPF_7D, 'hhexpf_7d.yaml'),
        (HHEXPNF_1M, 'hhexpnf_1m.yaml'),
        (HHEXPNF_6M, 'hhexpnf_6m.yaml'),
    ]

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

    output_dir = './reports'
    report_all_indicators_path = os.path.join(output_dir, 'HFC_All_Indicators_Report.xlsx')
    report_mastersheet_path = os.path.join(output_dir, 'HFC_MasterSheet_Report.xlsx')

    # Generate All Indicators Report
    with pd.ExcelWriter(report_all_indicators_path) as writer:
        current_df = read_data()
        # Specifically for DRC Since it is not standardized
        current_df = rename_columns(current_df)
        for indicator_class, config_file in indicators:
            standard_config_path = os.path.join(standard_config_dir, config_file)
            configurable_config_path = os.path.join(configurable_config_dir, config_file)
            standard_config = read_yaml(standard_config_path)
            configurable_config = read_yaml(configurable_config_path)

            instance = indicator_class(
                df=current_df,
                base_cols=base_cols,
                review_cols=review_cols,
                standard_config=standard_config,
                configurable_config=configurable_config,
                flags=indicator_class.flags
            )
            instance.process(writer)
            current_df = instance.df.copy()

    # Check if there were any errors and print the count
    error_count = error_handler.error_count
    if error_count > 0:
        print(f"Data processing completed with {error_count} errors.")
    else:
        print("Data processing completed successfully with no errors.")

    # Generate MasterSheet Report
    mastersheet = MasterSheet(current_df, base_cols, review_cols)
    new_mastersheet_df = mastersheet.generate_dataframe()

    final_mastersheet_df = MasterSheet.merge_with_existing_report(new_mastersheet_df, report_mastersheet_path)

    with pd.ExcelWriter(report_mastersheet_path) as writer:
        final_mastersheet_df.to_excel(writer, sheet_name='MasterSheet', index=False)