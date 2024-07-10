import pandas as pd
import logging
from high_frequency_checks.helpers.base_indicator import BaseIndicator
    
    
class HHEXPF_7D(BaseIndicator):
    """
    Calculates the monthly food expenditures for the last 7 days (HHExpF_7D) and checks if the monthly expenditures are zero.

    The `HHEXPF_7D` class inherits from the `BaseIndicator` class and performs the following tasks:

    1. Initializes the class with the necessary configuration parameters, including the column names for food purchases, gift aid, and own production.
    2. Implements the `_process_specific()` method, which is responsible for the specific processing of the HHExpF_7D indicator.
    3. The `calculate_monthly_hhexpf_7d()` method calculates the monthly food expenditures by summing the relevant columns and scaling the result to a monthly value.
    4. The `check_monthly_hhexpf_7d_zero()` method checks if the calculated monthly food expenditures are zero and sets a flag accordingly.
    """
                
    flags = {
        'Flag_HHEXPF_7D_Missing': "Missing value(s) in the Food Expenditures 7D Module",
        'Flag_HHEXPF_7D_Erroneous': "Erroneous value(s) in the Food Expenditures 7D Module",
        'Flag_HHEXPF_7D_Zero_FEXP': "No Food Purchases/GiftAid/OwnProduction Reported in the last 7 days"
    }
        
    def __init__(self, df, base_cols, review_cols, standard_config, configurable_config, flags):
        super().__init__(df, base_cols, review_cols, standard_config, configurable_config, flags)
        self.logger = logging.getLogger(__name__)
        self.hhexpf_7d_purch_cols = self.standard_config.get('hhexpf_7d_purch_cols', {})
        self.hhexpf_7d_giftaid_cols = self.standard_config.get('hhexpf_7d_giftaid_cols', {})
        self.hhexpf_7d_own_cols = self.standard_config.get('hhexpf_7d_own_cols', {})
        self.hhexpf_7d_cols = self.hhexpf_7d_purch_cols + self.hhexpf_7d_giftaid_cols + self.hhexpf_7d_own_cols
        
    def _process_specific(self):
        self.logger.info("Performing specific processing for HHExpF_7D indicator")
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous'] == 0
        self.calculate_monthly_hhexpf_7d(mask)
        self.check_monthly_hhexpf_7d_zero(mask)
        
    def calculate_monthly_hhexpf_7d(self, mask):
        self.logger.info("Calculating Monthly Expenditures for HHExpF_7D")
        try:
            newframe = pd.DataFrame()
            newframe['HHExpF_1M_Monthly'] = (self.df.loc[mask, self.hhexpf_7d_cols].sum(axis=1)) / 7 * 30
            self.df = pd.concat([self.df, newframe], axis=1)
            self.logger.info("Monthly Expenditures for HHExpF_7D calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating Monthly Expenditures for HHExpF_7D: {e}")
            
    def check_monthly_hhexpf_7d_zero(self, mask):
        self.logger.info(f"Checking if Monthly Expenditures for HHExpF_7D is Zero")
        try:
            newframe = pd.DataFrame()
            newframe['Flag_HHEXPF_7D_Zero_FEXP'] = (self.df.loc[mask, 'HHExpF_1M_Monthly'] == 0).astype(int)
            self.df = pd.concat([self.df, newframe], axis=1)
            self.logger.info(f"Generated Monthly Expenditures for HHExpF_7D is Zero flag")
        except Exception as e:
            self.logger.error(f"Error Checking if Monthly Expenditures for HHExpF_7D is Zero: {e}")