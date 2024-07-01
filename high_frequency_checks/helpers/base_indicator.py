import logging
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(filename='data_processing_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BaseIndicator:
    def __init__(self, df, base_cols, review_cols, standard_config, configurable_config, flags):

        self.df = df
        self.base_cols = base_cols
        self.review_cols = review_cols
        self.standard_config = standard_config
        self.configurable_config = configurable_config
        self.cols_type = self.standard_config.get('columns_type', {})
        self.indicator_name = self.__class__.__name__
        self.flags = flags
        self.low_erroneous = self.configurable_config.get('low_erroneous', None) if configurable_config else None
        self.high_erroneous = self.configurable_config.get('high_erroneous', None) if configurable_config else None
        self.logger = logging.getLogger(__name__)
        
        if self.indicator_name in ['LCS_FS', 'LCS_FS_R', 'LCS_EN']:
            used_strategies = self.configurable_config.get('used_strategies', [])
            self.cols = [col for col in self.cols_type.keys() if col in used_strategies and col in self.df.columns]
        else:
            self.cols = list(self.cols_type.keys())

    def parse_columns(self):
        self.logger.info(f"Parsing columns with standard_config: {self.cols_type}")
        for col, expected_type in self.cols_type.items():
            if col in self.df.columns and col in self.cols:
                try:
                    if expected_type == 'int':
                        # Convert to Int64Dtype which supports NaN
                        self.df[col] = pd.to_numeric(self.df[col], errors='coerce').astype(pd.Int64Dtype())
                    elif expected_type == 'float':
                        self.df[col] = pd.to_numeric(self.df[col], errors='coerce').astype(float)
                    elif expected_type == 'str':
                        self.df[col] = self.df[col].astype(object)
                    else:
                        self.logger.warning(f"Column '{col}' has an unexpected type: {self.df[col].dtype}")
                    self.logger.info(f"Column '{col}' converted to type {expected_type}. Current type: {self.df[col].dtype}")
                except Exception as e:
                    self.logger.error(f"Error converting column '{col}' to type {expected_type}: {e}")
            else:
                if self.indicator_name in ['HHEXPF_7D', 'HHEXPNF_1M', 'HHEXPNF_6M']:
                    self.logger.warning(f"Column '{col}' not found in the DataFrame. an empty column for {col} will be created.")
                    self.df[col] = np.nan
                else:
                    self.logger.warning(f"Column '{col}' not found in the DataFrame")
                
    def check_missing_values(self):
        self.logger.info(f'Checking missing values for {self.indicator_name}')
        try:
            conditional_cols_integer = []
            conditional_cols_categorical = []
            unconditional_cols = []
            
            # Determine categorical and integer columns based on choices_lists
            if 'conditional_pairs_integer' in self.standard_config and 'conditional_pairs_categorical' in self.standard_config:
                for col in self.cols:
                    if col in self.standard_config['conditional_pairs_integer']:
                        conditional_cols_integer.append(col)
                    elif col in self.standard_config['conditional_pairs_categorical']:
                        conditional_cols_categorical.append(col)
                    else:
                        unconditional_cols.append(col)
                        
            elif 'conditional_pairs_integer' in self.standard_config and 'conditional_pairs_categorical' not in self.standard_config:
                for col in self.cols:
                    if col in self.standard_config['conditional_pairs_integer']:
                        conditional_cols_integer.append(col)
                    else:
                        unconditional_cols.append(col)   
            
            elif 'conditional_pairs_integer' not in self.standard_config and 'conditional_pairs_categorical' in self.standard_config:
                for col in self.cols:
                    if col in self.standard_config['conditional_pairs_categorical']:
                        conditional_cols_categorical.append(col)
                    else:
                        unconditional_cols.append(col)
                        
            else:
                unconditional_cols = self.cols
                    
            # Initialize the missing flag column
            missing_flag_col = pd.Series(0, index=self.df.index, name=f'Flag_{self.indicator_name}_Missing')

            # Check missing values for unconditional columns
            if unconditional_cols:
                missing_condition = self.df[unconditional_cols].isnull().any(axis=1)
                missing_flag_col[missing_condition] = 1
                self.logger.info(f"Generated missing value flags for unconditional columns: {unconditional_cols}")

            # Check missing values conditionally for conditional columns that are integer
            if conditional_cols_integer:
                for col in conditional_cols_integer:
                    pair_cols = self.standard_config['conditional_pairs_integer'].get(col)
                    condition_mask = self.df[pair_cols].gt(0).any(axis=1)
                    missing_condition = condition_mask & self.df[col].isnull()
                    missing_flag_col[missing_condition] = 1
                self.logger.info(f"Generated missing value flags for conditional columns: {conditional_cols_integer}")

            # Check missing values conditionally for conditional columns that are categorical
            if conditional_cols_categorical:
                for col in conditional_cols_categorical:
                    pair_cols = self.standard_config['conditional_pairs_categorical'].get(col)
                    condition_mask = self.df[pair_cols].eq('1').any(axis=1)
                    missing_condition = condition_mask & self.df[col].isnull()
                    missing_flag_col[missing_condition] = 1
                self.logger.info(f"Generated missing value flags for conditional columns: {conditional_cols_categorical}")

            # Concatenate missing_flag_col to self.df
            self.df = pd.concat([self.df, missing_flag_col], axis=1)


        except Exception as e:
            self.logger.error(f"Error in check_missing_values method: {e}")
            
    def check_erroneous_values(self):
        self.logger.info(f"Checking erroneous values for {self.indicator_name}")
        try:
            int_cols = []
            categorical_cols = []
            
            # Determine categorical and integer columns based on choices_lists
            if 'choices_lists' in self.standard_config:
                for col in self.cols:
                    if col in self.standard_config['choices_lists']:
                        categorical_cols.append(col)
                    else:
                        int_cols.append(col)
            else:
                int_cols = self.cols
                
            # Initialize the erroneous flag column
            erroneous_flag_col = pd.Series(np.nan, index=self.df.index, name=f'Flag_{self.indicator_name}_Erroneous')
            mask = self.df[f'Flag_{self.indicator_name}_Missing'] == 0

            # Check erroneous values for categorical columns
            if categorical_cols:
                for col in categorical_cols:
                    choices = self.standard_config['choices_lists'].get(col, [])
                    if choices:
                        erroneous_condition = (~self.df[col].isin(choices)).astype(int)
                        erroneous_flag_col[mask & (erroneous_flag_col != 1)] = erroneous_condition
                        self.logger.info(f"Generated erroneous value flags for categorical column: {col}")
                    else:
                        self.logger.warning(f"No choices defined for column '{col}' in choices_lists.")

            # Check erroneous values for integer columns
            if int_cols:
                erroneous_condition = ((self.df[int_cols] < self.low_erroneous) | (self.df[int_cols] > self.high_erroneous))
                erroneous_condition = erroneous_condition.any(axis=1).astype(int)
                erroneous_flag_col[mask & (erroneous_flag_col != 1)] = erroneous_condition
                self.logger.info(f"Generated erroneous value flags for integer columns: {int_cols}")

            # Concatenate erroneous_flag_col to self.df
            self.df = pd.concat([self.df, erroneous_flag_col], axis=1)

        except Exception as e:
            self.logger.error(f"Error in check_erroneous_values method: {e}")


    def generate_overall_flag(self):
        self.logger.info(f"Calculating overall flag for {self.indicator_name}")
        try:
            flag_name = f'Flag_{self.indicator_name}_Overall'
            overall_flag = self.df[list(self.flags.keys())].any(axis=1)
            self.df[flag_name] = overall_flag.astype(int)
            self.logger.info(f"Generated an overall flag for {self.indicator_name}")
        except Exception as e:
            self.logger.error(f"Error in generate_overall_flag method: {e}")

    def generate_narrative_flag(self):
        self.logger.info(f"Combining flags into one narrative flag for {self.indicator_name}")
        try:
            narrative_flags = list(self.flags.keys())
            self.df[f'Flag_{self.indicator_name}_Narrative'] = self.df[narrative_flags].apply(
                lambda row: " & ".join([self.flags[flag] for flag in narrative_flags if row[flag] == 1]), axis=1
            )
            self.logger.info(f"Generated a narrative flag for {self.indicator_name}")
        except Exception as e:
            self.logger.error(f"Error in generate_narrative_flag method: {e}")

    def generate_report(self, writer: pd.ExcelWriter):
        self.logger.info(f"Generating report for {self.indicator_name}")
        try:
            hh_summary_cols = self.base_cols + self.cols + list(self.flags.keys()) + [f'Flag_{self.indicator_name}_Overall', f'Flag_{self.indicator_name}_Narrative']
            hh_summary = self.df[hh_summary_cols]
            hh_filtered = hh_summary[hh_summary[f'Flag_{self.indicator_name}_Overall'] == 1]
            hh_filtered.to_excel(writer, sheet_name=self.indicator_name, index=False)
            self.logger.info(f"Report for {self.indicator_name} generated successfully")
        except Exception as e:
            self.logger.error(f"Error generating report for {self.indicator_name}: {e}")

    def process(self, writer):
        if len(self.cols) > 0:
            self.parse_columns()
            if self.indicator_name in ['LCS_FS', 'LCS_FS_R', 'LCS_EN']:
                self.df[f'Flag_{self.indicator_name}_Missing'] = 0
                self.df[f'Flag_{self.indicator_name}_Erroneous'] = 0
            else:
                self.check_missing_values()
                self.check_erroneous_values()
            self._process_specific()
            self.generate_overall_flag()
            self.generate_narrative_flag()
            self.generate_report(writer)

    def _process_specific(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def calculate_indicators(self):
        pass

    def generate_flags(self):
        pass

