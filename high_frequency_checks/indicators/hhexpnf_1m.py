import logging
from high_frequency_checks.helpers.base_indicator import BaseIndicator
    
    
class HHEXPNF_1M(BaseIndicator):
    """
    Calculates the monthly non-food expenditures for a household based on the provided data.

    The HHEXPNF_1M class is responsible for processing the non-food expenditures data for a 1-month period. It calculates the total monthly non-food expenditures by summing the values in the `hhexpnf_1m_purch_cols` and `hhexpnf_1m_giftaid_cols` columns, and stores the result in the `HHExpNF_1M_Monthly` column. The class also handles missing and erroneous values in the data.
    """
                
    flags = {
        'Flag_HHEXPNF_1M_Missing': "Missing value(s) in the Non-Food Expenditures 1M Module",
        'Flag_HHEXPNF_1M_Erroneous': "Non-Food Expenditures 1M Module has invalid range of values (negative or above max thresholds)",
    }
        
    def __init__(self, df, base_cols, review_cols, standard_config, configurable_config, flags):
        super().__init__(df, base_cols, review_cols, standard_config, configurable_config, flags)
        self.logger = logging.getLogger(__name__)
        self.hhexpnf_1m_purch_cols = self.standard_config.get('hhexpnf_1m_purch_cols', {})
        self.hhexpnf_1m_giftaid_cols = self.standard_config.get('hhexpnf_1m_giftaid_cols', {})
        self.hhexpnf_1m_cols = self.hhexpnf_1m_purch_cols + self.hhexpnf_1m_giftaid_cols
        
    def _process_specific(self):
        self.logger.info("Performing specific processing for HHExpNF_1M indicator")
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous'] == 0
        self.calculate_monthly_hhexpnf_1M(mask)
        
    def calculate_monthly_hhexpnf_1M(self, mask):
        self.logger.info("Calculating Monthly Expenditures for HHExpNF_1M")
        try:
            self.df.loc[mask, 'HHExpNF_1M_Monthly'] = (self.df.loc[mask, self.hhexpnf_1m_cols].sum(axis=1))
            self.logger.info("Monthly Expenditures for HHExpNF_1M calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating Monthly Expenditures for HHExpNF_1M: {e}")
            