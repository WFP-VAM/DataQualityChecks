import pandas as pd
from indicators.fcs import FCS
from indicators.rcsi import rCSI
from indicators.demographics import Demo
from indicators.hdds import HDDS
from indicators.fexp_7d import FEXP_7D
from indicators.nfexp_1m import NFEXP_1M
from indicators.nfexp_6m import NFEXP_6M
from mastersheet.mastersheet import MasterSheet
from config import config

# List of Indicator Classes
indicators = [
    (Demo, 'Demo'),
    (FCS, 'FCS'),
    (rCSI, 'rCSI'),
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
    report_path = f'{output_dir}/HFC_Report.xlsx'

    with pd.ExcelWriter(report_path) as writer:
        current_df = df.copy()
        for indicator_class, config_key in indicators:
            config_values = config[config_key]
            instance = indicator_class(current_df, **config_values)
            process_indicator(instance, writer)
            current_df = instance.df.copy()  # Update current_df for the next indicator

        mastersheet = MasterSheet(current_df)
        mastersheet.generate_report(writer)
