import logging
from high_frequency_checks.helpers.base_indicator import BaseIndicator
    
    
class HHEXPNF_6M(BaseIndicator):
    """
    Calculates the monthly non-food expenditures for the household over a 6-month period.

    This class extends the `BaseIndicator` class and provides methods to process and calculate the monthly non-food expenditures for a household. It uses the standard and configurable configurations to determine the relevant columns for the calculation.

    The class also defines two flags: `Flag_HHEXPNF_6M_Missing` and `Flag_HHEXPNF_6M_Erroneous`, which are used to indicate missing or erroneous values in the non-food expenditures 6-month module.
    """
        
        
    flags = {
        'Flag_HHEXPNF_6M_Missing': "Missing value(s) in the Non-Food Expenditures 6M Module",
        'Flag_HHEXPNF_6M_Erroneous': "Non-Food Expenditures 6M Module has invalid range of values (negative or above max thresholds)",
    }
        
    def __init__(self, df, base_cols, standard_config, configurable_config, flags):
        super().__init__(df, base_cols, standard_config, configurable_config, flags)
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
            