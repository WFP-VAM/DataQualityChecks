import logging
from high_frequency_checks.helpers.base_indicator import BaseIndicator

    
class LCS_EN(BaseIndicator):
    """
    Implements the LCS-EN (Livelihood Coping Strategies - English) indicator, which checks for various issues in the livelihood coping strategies data.

    The indicator performs the following checks:
    - Checks if there are any children-related livelihood coping strategies reported in households with no children.
    - Checks if there are three or more livelihood coping strategies reported as N/A.
    - Checks if any non-exhaustive livelihood coping strategies are reported as N/A or exhausted.

    The indicator uses a set of predefined flags to report the issues found in the data.
    """
                
    flags = {
    'Flag_LCS_EN_Missing': "LCS-EN: Missing value(s) in the livelihood coping strategies",
    'Flag_LCS_EN_Erroneous': "LCS-EN: choice list not matching standard Codebook choices - please review choice list in DataBridges",
    'Flag_LCS_EN_No_Children': "LCS-EN: HH Applied strategies related to children with no children",
    'Flag_LCS_EN_Three_or_More_NA': "LCS-EN: Three or more livelihood coping strategies reported as NA",
    'Flag_LCS_EN_NonExhaustive_Strategies_NA': "LCS-EN: HH reported as exhausted or not applicable coping strategies that cannot be exhausted or not applicable (e.g. illegal activities, begging)"
    }
        
    def __init__(self, df, base_cols, review_cols, standard_config, configurable_config, flags):
        super().__init__(df, base_cols, review_cols, standard_config, configurable_config, flags)
        self.logger = logging.getLogger(__name__)
        self.lcs_children_cols = list(self.standard_config.get('lcs_en_children_cols', {}))
        self.lcs_non_exhaustive_cols = list(self.standard_config.get('lcs_en_non_exhaustive_cols', {}))

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
                self.df.loc[mask, f'Flag_{self.indicator_name}_No_Children'] = (
                    (self.df['Sum_Children'] == 0) & 
                    self.df[children_cols_present].isin(['20', '30']).any(axis=1)
                ).astype(int)
            else:
                self.df.loc[mask, f'Flag_{self.indicator_name}_No_Children'] = 0
            self.logger.info("Generated children strategies with no children in HH flag")
        except Exception as e:
            self.logger.error(f"Error checking children strategies with no children in HH: {e}")

    def check_three_or_more_na(self, mask):
        self.logger.info("Checking for three or more N/A in strategies")
        try:
            self.df.loc[mask, f'Flag_{self.indicator_name}_Three_or_More_NA'] = (
                (self.df[self.cols] == '9999').sum(axis=1) >= 3
            ).astype(int)
            self.logger.info("Generated three or more N/A in strategies flag")
        except Exception as e:
            self.logger.error(f"Error checking three or more N/A in strategies: {e}")

    def check_non_exhaustive_strategies_na(self, mask):
        self.logger.info("Checking for non-exhaustive strategies reported as N/A or exhausted")
        try:
            non_exhaustive_cols_present = [col for col in self.lcs_non_exhaustive_cols if col in self.df.columns]
            if non_exhaustive_cols_present:
                self.df.loc[mask, f'Flag_{self.indicator_name}_NonExhaustive_Strategies_NA'] = (
                    self.df[non_exhaustive_cols_present].isin(['30', '9999']).any(axis=1)
                ).astype(int)
            else:
                self.df.loc[mask, f'Flag_{self.indicator_name}_NonExhaustive_Strategies_NA'] = 0
            self.logger.info("Generated non-exhaustive strategies N/A flag")
        except Exception as e:
            self.logger.error(f"Error checking non-exhaustive strategies reported as N/A or exhausted: {e}")
