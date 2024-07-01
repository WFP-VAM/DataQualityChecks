import logging
from high_frequency_checks.helpers.base_indicator import BaseIndicator
    
    
class HHEXPF_7D(BaseIndicator):
    
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
            self.df.loc[mask, 'HHExpF_1M_Monthly'] = (self.df.loc[mask, self.hhexpf_7d_cols].sum(axis=1)) / 7 * 30
            self.logger.info("Monthly Expenditures for HHExpF_7D calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating Monthly Expenditures for HHExpF_7D: {e}")
            
    def check_monthly_hhexpf_7d_zero(self, mask):
        self.logger.info(f"Checking if Monthly Expenditures for HHExpF_7D is Zero")
        try:
            self.df.loc[mask, 'Flag_HHEXPF_7D_Zero_FEXP'] = (self.df.loc[mask, 'HHExpF_1M_Monthly'] == 0).astype(int)
            self.logger.info(f"Generated Monthly Expenditures for HHExpF_7D is Zero flag")
        except Exception as e:
            self.logger.error(f"Error Checking if Monthly Expenditures for HHExpF_7D is Zero: {e}")
