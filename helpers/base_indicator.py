import pandas as pd
import numpy as np
from datetime import datetime

today = datetime.now().strftime("%Y%m%d")  

class BaseIndicator:
    def __init__(self, df, indicator_name, cols, flags, weights=None):
        self.df = df
        self.cols = cols
        self.flags = flags
        self.weights = weights
        self.indicator_name = indicator_name
        self._validate_columns()
        self.df[f'Flag_{self.indicator_name}'] = np.nan  # Overall flag initialization
        self.df[f'Flag_{self.indicator_name}_Narrative'] = ''   # Narrative flag initialization

    def _validate_columns(self):
        required_columns = ['EnuName', 'ID02'] + self.cols
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            raise KeyError(f"The following required columns are missing from the DataFrame: {', '.join(missing_columns)}")

    def custom_flag_logic(self):
        # Placeholder for custom flag logic, to be implemented in derived classes
        pass

    def generate_flags(self):
        print(f"Generating flags for {self.indicator_name}...")
        for flag in self.flags.keys():
            self.df[f'Flag_{self.indicator_name}_{flag}'] = np.nan

        # Missing Values
        self.df[f'Flag_{self.indicator_name}_Missing_Values'] = self.df[self.cols].isnull().any(axis=1).astype(int)

        # Erroneous Values
        erroneous_condition = (self.df[self.cols] < 0) | (self.df[self.cols] > 7)
        self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] = np.where(
            (self.df[f'Flag_{self.indicator_name}_Missing_Values'].fillna(0) == 0) & erroneous_condition.any(axis=1),
            1, 0
        )

        self.custom_flag_logic()

        # Overall Flag
        base_flags = [f'Flag_{self.indicator_name}_{flag}' for flag in self.flags.keys() if not flag.startswith('Flag_FCS_')]
        custom_flags = [col for col in self.df.columns if col.startswith(f'Flag_{self.indicator_name}_')]
        overall_flag = self.df[base_flags + custom_flags].any(axis=1)
        self.df[f'Flag_{self.indicator_name}'] = overall_flag.astype(int)

        # Generate Narrative Flags
        self.generate_narrative_flags()

    def generate_narrative_flags(self):
        print(f"Generating narrative flags for {self.indicator_name}...")
        narrative_flags = list(self.flags.keys())[:-1]

        self.df[f'Flag_{self.indicator_name}_Narrative'] = self.df[narrative_flags].apply(
            lambda row: " & ".join([self.flags[flag] for flag in narrative_flags if row[flag] == 1]), axis=1
        )

    def generate_report(self, output_dir, additional_cols=[]):
        print(f"Generating report for {self.indicator_name}...")
        hh_summary_cols = ['EnuName'] + self.cols + additional_cols + list(self.flags.keys()) + [f'Flag_{self.indicator_name}', f'Flag_{self.indicator_name}_Narrative']

        hh_summary = self.df[hh_summary_cols]

        enu_summary = self.summarize_flags('EnuName')
        enu_summary = enu_summary[enu_summary['Error_Percentage'] >= 0.1].sort_values(by='Error_Percentage', ascending=True)

        id02_enu_summary = self.summarize_flags(['ID02', 'EnuName'])
        id02_enu_summary = id02_enu_summary.reset_index()

        with pd.ExcelWriter(f'{output_dir}/{today}_{self.indicator_name}_Report.xlsx') as writer:
            hh_summary.to_excel(writer, sheet_name='HH_Report', index=False)
            enu_summary.to_excel(writer, sheet_name='Enu_Report', index=False)
            id02_enu_summary.to_excel(writer, sheet_name='Admin2_Enu_Report', index=False)

    def summarize_flags(self, group_by_cols):
        print("Summarizing flags...")
        summary = self.df.groupby(group_by_cols).agg({flag: 'sum' for flag in [f'Flag_{self.indicator_name}_{flag}' for flag in self.flags.keys() if not flag.startswith('Flag_FCS_')]})
        summary['Total'] = summary.sum(axis=1)
        summary['Error_Percentage'] = (summary['Total'] / len(self.df)) * 100
        summary = summary.reset_index()
        return summary
