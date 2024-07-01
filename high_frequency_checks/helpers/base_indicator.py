import numpy as np
import pandas as pd
from .standard.base_indicator import base_cols
import logging

logname = "logs/HFC.log"

logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


class BaseIndicator:
    
    def __init__(self, 
                 df: pd.DataFrame,
                 indicator_name: str,
                 cols: list,
                 flags: dict, 
                 exclude_missing_check: list = None, 
                 exclude_erroneous_check: list = None):
        
        self.df = df
        self.indicator_name = indicator_name
        self.cols = cols
        self.base_cols = base_cols
        self.flags = flags
        self.exclude_missing_check = exclude_missing_check or []
        self.exclude_erroneous_check = exclude_erroneous_check or []

        self.initialize_flags()
        self.parse_columns()

    def initialize_flags(self):
        self.df[f'Flag_{self.indicator_name}_Overall'] = np.nan
        self.df[f'Flag_{self.indicator_name}_Narrative'] = ''

    def validate_columns(self):
        required_columns = self.base_cols + self.cols
        missing_columns = [col for col in required_columns if col not in self.df.columns]

        if missing_columns:
            raise KeyError(f"Missing columns: {', '.join(missing_columns)}")
    
    def parse_columns(self):
        for col in self.cols:
            self.df[col] =  pd.to_numeric(self.df[col], errors='ignore')
        pass
    
    def generate_flags(self):
        logging.info(f"Generating flags for {self.indicator_name}")
        self.initialize_individual_flags()
        self.generate_missing_value_flags()
        self.generate_erroneous_value_flags()
        self.custom_flag_logic()
        self.generate_overall_flag()
        self.generate_narrative_flag()

    def initialize_individual_flags(self):
        for flag in self.flags:
            self.df[flag] = np.nan

    def generate_missing_value_flags(self):
        check_cols = [col for col in self.cols if col not in self.exclude_missing_check]
        self.df[f'Flag_{self.indicator_name}_Missing_Values'] = self.df[check_cols].isnull().any(axis=1).astype(int)

    def generate_erroneous_value_flags(self):
        check_cols = [col for col in self.cols if col not in self.exclude_erroneous_check]
        erroneous_condition = (self.df[check_cols] < self.low_erroneous) | (self.df[check_cols] > self.high_erroneous)
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Missing_Values'] == 0, f'Flag_{self.indicator_name}_Erroneous_Values'] = erroneous_condition.any(axis=1).astype(int)

    def custom_flag_logic(self):
        pass

    def generate_overall_flag(self):
        overall_flag = self.df[self.flags.keys()].any(axis=1)
        self.df[f'Flag_{self.indicator_name}_Overall'] = overall_flag.astype(int)

    def generate_narrative_flag(self):
        logging.info(f"Generating narrative flags for {self.indicator_name}")
        narrative_flags = list(self.flags.keys())
        
        self.df[f'Flag_{self.indicator_name}_Narrative'] = self.df[narrative_flags].apply(
            lambda row: " & ".join([self.flags[flag] for flag in narrative_flags if row[flag] == 1]), axis=1
        )

    def generate_report(self, writer: pd.ExcelWriter):
        logging.info(f"Generating report for {self.indicator_name}")
        hh_summary_cols = self.base_cols + self.cols + list(self.flags.keys()) + [f'Flag_{self.indicator_name}_Overall', f'Flag_{self.indicator_name}_Narrative']
        hh_summary = self.df[hh_summary_cols]
        hh_filtered = hh_summary[hh_summary[f'Flag_{self.indicator_name}_Overall'] == 1]
        hh_filtered.to_excel(writer, sheet_name=self.indicator_name, index=False)
