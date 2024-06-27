import numpy as np


class BaseIndicator:
    def __init__(self, df, indicator_name, cols, flags, weights=None, exclude_missing_check=None):
        self.df = df
        self.cols = cols
        self.flags = flags
        self.weights = weights
        self.indicator_name = indicator_name
        self.exclude_missing_check = exclude_missing_check if exclude_missing_check else []
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
        check_cols = [col for col in self.cols if col not in self.exclude_missing_check]
        self.df[f'Flag_{self.indicator_name}_Missing_Values'] = self.df[check_cols].isnull().any(axis=1).astype(int)

        # Erroneous Values
        print(f"Erroneous value parameters for {self.indicator_name}: low = {self.low_erroneous}, high = {self.high_erroneous}")
        erroneous_condition = (self.df[self.cols] < self.low_erroneous) | (self.df[self.cols] > self.high_erroneous)
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Missing_Values'] == 0, f'Flag_{self.indicator_name}_Erroneous_Values'] = erroneous_condition.any(axis=1).astype(int)

        self.custom_flag_logic()

        # Overall Flag
        base_flags = [f'Flag_{self.indicator_name}_{flag}' for flag in self.flags.keys() if not flag.startswith('Flag_FCS_')]
        custom_flags = [col for col in self.df.columns if col.startswith(f'Flag_{self.indicator_name}_')]
        overall_flag = self.df[base_flags + custom_flags].any(axis=1)
        self.df[f'Flag_{self.indicator_name}_Overall'] = overall_flag.astype(int)

        # Generate Narrative Flags
        self.generate_narrative_flags()

    def generate_narrative_flags(self):
        print(f"Generating narrative flags for {self.indicator_name}")
        narrative_flags = list(self.flags.keys())

        self.df[f'Flag_{self.indicator_name}_Narrative'] = self.df[narrative_flags].apply(
            lambda row: " & ".join([self.flags[flag] for flag in narrative_flags if row[flag] == 1]), axis=1
        )
                        
    def generate_report(self, writer):
        print(f"Generating report for {self.indicator_name}")
        hh_summary_cols = ['_uuid', 'EnuName', 'EnuSupervisorName', 'ID01', 'ID02', 'ID03', 'ID04'] + self.cols + list(self.flags.keys()) + [f'Flag_{self.indicator_name}_Overall', f'Flag_{self.indicator_name}_Narrative']
        hh_summary = self.df[hh_summary_cols]
        
        # Filtering the Summary Dataset to include only Household with triggered flags
        hh_filtered = hh_summary[hh_summary[f'Flag_{self.indicator_name}_Overall'] == 1]
        hh_filtered.to_excel(writer, sheet_name=self.indicator_name, index=False)           
