import logging
from high_frequency_checks.helpers.base_indicator import BaseIndicator
    
    
class HHEXPNF_6M(BaseIndicator):
    
    flags = {
        'Flag_HHEXPNF_6M_Missing': "Missing value(s) in the Non-Food Expenditures 6M Module",
        'Flag_HHEXPNF_6M_Erroneous': "Erroneous value(s) in the Non-Food Expenditures 6M Module",
    }
        
    def __init__(self, df, base_cols, review_cols, standard_config, configurable_config, flags):
        super().__init__(df, base_cols, review_cols, standard_config, configurable_config, flags)
        self.logger = logging.getLogger(__name__)
        self.hhexpnf_6m_purch_cols = self.standard_config.get('hhexpnf_6m_purch_cols', {})
        self.hhexpnf_6m_giftaid_cols = self.standard_config.get('hhexpnf_6m_giftaid_cols', {})
        self.hhexpnf_6m_cols = self.hhexpnf_6m_purch_cols + self.hhexpnf_6m_giftaid_cols
        
    def _process_specific(self):
        self.logger.info("Performing specific processing for HHExpNF_6M indicator")
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous'] == 0
        self.calculate_monthly_hhexpnf_6M(mask)
        
    def calculate_monthly_hhexpnf_6M(self, mask):
        self.logger.info("Calculating Monthly Expenditures for HHExpNF_6M")
        try:
            self.df.loc[mask, 'HHExpNF_6M_Monthly'] = (self.df.loc[mask, self.hhexpnf_6m_cols].sum(axis=1))
            self.logger.info("Monthly Expenditures for HHExpNF_6M calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating Monthly Expenditures for HHExpNF_6M: {e}")
            