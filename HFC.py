import pandas as pd
from high_frequency_checks import FCS, rCSI, Demo, HDDS, FEXP_7D, NFEXP_1M, NFEXP_6M, LCS, MasterSheet
from config import config


# List of Indicator Classes
indicators = [
    (Demo, 'Demo'),
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
    instance.calculate_indicators()
    instance.generate_flags()
    instance.generate_report(writer)

if __name__ == "__main__":
    df = pd.read_csv('data/congo.csv')
    output_dir = './Reports'
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
