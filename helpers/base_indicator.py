import pandas as pd
import numpy as np

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
        print(f"Generating flags for {self.indicator_name}")
        for flag in self.flags.keys():
            self.df[f'Flag_{self.indicator_name}_{flag}'] = np.nan

        # Missing Values
        self.df[f'Flag_{self.indicator_name}_Missing_Values'] = self.df[self.cols].isnull().any(axis=1).astype(int)

        # Erroneous Values
        print(f"Erroneous value parameters for {self.indicator_name}: low = {self.low_erroneous}, high = {self.high_erroneous}")
        erroneous_condition = (self.df[self.cols] < self.low_erroneous) | (self.df[self.cols] > self.high_erroneous)
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Missing_Values'] == 0, f'Flag_{self.indicator_name}_Erroneous_Values'] = erroneous_condition.any(axis=1).astype(int)

        self.custom_flag_logic()

        # Overall Flag
        base_flags = [f'Flag_{self.indicator_name}_{flag}' for flag in self.flags.keys() if not flag.startswith('Flag_FCS_')]
        custom_flags = [col for col in self.df.columns if col.startswith(f'Flag_{self.indicator_name}_')]
        overall_flag = self.df[base_flags + custom_flags].any(axis=1)
        self.df[f'Flag_{self.indicator_name}'] = overall_flag.astype(int)

        # Generate Narrative Flags
        self.generate_narrative_flags()

    def generate_narrative_flags(self):
        print(f"Generating narrative flags for {self.indicator_name}")
        narrative_flags = list(self.flags.keys())

        self.df[f'Flag_{self.indicator_name}_Narrative'] = self.df[narrative_flags].apply(
            lambda row: " & ".join([self.flags[flag] for flag in narrative_flags if row[flag] == 1]), axis=1
        )

    def generate_report(self, output_dir, additional_cols=[]):
        print(f"Generating report for {self.indicator_name}")
        hh_summary_cols = ['EnuName'] + self.cols + additional_cols + list(self.flags.keys()) + [f'Flag_{self.indicator_name}', f'Flag_{self.indicator_name}_Narrative']

        hh_summary = self.df[hh_summary_cols]

        with pd.ExcelWriter(f'{output_dir}/{self.indicator_name}_Report.xlsx') as writer:
            hh_summary.to_excel(writer, sheet_name='HH_Report', index=False)

