import logging
from high_frequency_checks.helpers.base_indicator import BaseIndicator
    
class LCS(BaseIndicator):
    
    flags = {
    'Flag_LCS_Missing': "Missing value(s) in the livelihood coping strategies",
    'Flag_LCS_Erroneous': "Erroneous value(s) in the livelihood coping strategies",
    'Flag_LCS_No_Children': "HH Applied strategies related to children with no children",
    'Flag_LCS_Three_or_More_NA': "Three or more livelihood coping strategies reported as NA",
    'Flag_LCS_NonExhaustive_Strategies_NA': "HH Reported activities that can't be exhausted as exhausted or Not Applicable"
    }
        
    def __init__(self, df, base_cols, review_cols, standard_config, configurable_config, flags):
        super().__init__(df, base_cols, review_cols, standard_config, configurable_config, flags)
        self.logger = logging.getLogger(__name__)
        self.lcs_stress_cols = [col for col in list(self.standard_config.get('lcs_stress_cols', {})) if col in self.df.columns]
        self.lcs_crisis_cols = [col for col in list(self.standard_config.get('lcs_crisis_cols', {})) if col in self.df.columns]
        self.lcs_em_cols = [col for col in list(self.standard_config.get('lcs_em_cols', {})) if col in self.df.columns]
        # self.cols = self.lcs_stress_cols + self.lcs_crisis_cols + self.lcs_em_cols
        self.lcs_children_cols = list(self.standard_config.get('lcs_children_cols', {}))
        self.lcs_non_exhaustive_cols = list(self.standard_config.get('lcs_non_exhaustive_cols', {}))

    def _process_specific(self):
        self.logger.info("Performing specific processing for Demo indicator")
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous'] == 0
        self.check_no_children(mask)
        self.check_three_or_more_na(mask)
        self.check_non_exhaustive_strategies_na(mask)
       
    def check_no_children(self, mask):
        self.logger.info("Checking for children strategies with no children in HH")
        try:
            children_cols_present = [col for col in self.lcs_children_cols if col in self.df.columns]
            if children_cols_present:
                self.df.loc[mask, 'Flag_LCS_No_Children'] = (
                    (self.df['Sum_children'] == 0) & 
                    self.df[children_cols_present].isin(['20', '30']).any(axis=1)
                ).astype(int)
            else:
                self.df.loc[mask, 'Flag_LCS_No_Children'] = 0
            self.logger.info("Generated children strategies with no children in HH flag")
        except Exception as e:
            self.logger.error(f"Error checking children strategies with no children in HH: {e}")

    def check_three_or_more_na(self, mask):
        self.logger.info("Checking for three or more N/A in strategies")
        try:
            self.df.loc[mask, f'Flag_LCS_Three_or_More_NA'] = (
                (self.df[self.cols] == 9999).sum(axis=1) >= 3
            ).astype(int)
            self.logger.info("Generated three or more N/A in strategies flag")
        except Exception as e:
            self.logger.error(f"Error checking three or more N/A in strategies: {e}")

    def check_non_exhaustive_strategies_na(self, mask):
        self.logger.info("Checking for non-exhaustive strategies reported as N/A or exhausted")
        try:
            non_exhaustive_cols_present = [col for col in self.lcs_non_exhaustive_cols if col in self.df.columns]
            if non_exhaustive_cols_present:
                self.df.loc[mask, f'Flag_LCS_NonExhaustive_Strategies_NA'] = (
                    self.df[non_exhaustive_cols_present].isin(['30', '9999']).any(axis=1)
                ).astype(int)
            else:
                self.df.loc[mask, f'Flag_LCS_NonExhaustive_Strategies_NA'] = 0
            self.logger.info("Generated non-exhaustive strategies N/A flag")
        except Exception as e:
            self.logger.error(f"Error checking non-exhaustive strategies reported as N/A or exhausted: {e}")
