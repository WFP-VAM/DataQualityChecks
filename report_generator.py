# report_generator.py
import pandas as pd
import os
from high_frequency_checks.helpers.customize import rename_columns
from high_frequency_checks.mastersheet import MasterSheet
from config_handler import get_base_config, get_indicator_config
from data_retriever import read_data

def generate_all_indicators_report(indicators, output_path):
    with pd.ExcelWriter(output_path) as writer:
        current_df = read_data()
        current_df = rename_columns(current_df)

        for indicator_class, config_file in indicators:
            standard_config, configurable_config = get_indicator_config(config_file)

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

def generate_mastersheet_report(current_df, output_path):
    mastersheet = MasterSheet(current_df, base_cols, review_cols)
    new_mastersheet_df = mastersheet.generate_dataframe()

    final_mastersheet_df = MasterSheet.merge_with_existing_report(new_mastersheet_df, output_path)

    with pd.ExcelWriter(output_path) as writer:
        final_mastersheet_df.to_excel(writer, sheet_name='MasterSheet', index=False)
