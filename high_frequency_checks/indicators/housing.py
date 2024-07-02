import logging
from high_frequency_checks.helpers.base_indicator import BaseIndicator
    
    
class Housing(BaseIndicator):
        
    flags = {
        'Flag_Housing_Missing': "Missing value(s) in the Housing Module",
        'Flag_Housing_Erroneous': "Erroneous value(s) in the Housing Module",
        'Flag_Housing_Displaced_Owner': "HH is displaced and own a residential property"
    }
        
    def __init__(self, df, base_cols, review_cols, standard_config, configurable_config, flags):
        super().__init__(df, base_cols, review_cols, standard_config, configurable_config, flags)
        self.logger = logging.getLogger(__name__)
        
    def _process_specific(self):
        self.logger.info("Performing specific processing for Housing indicator")
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous'] == 0
        self.check_displaced_owner(mask)

    def check_displaced_owner(self, mask):
        self.logger.info("Checking for Displaced HHs who own a residential property")
        try:
            self.df.loc[mask, f'Flag_Housing_Displaced_Owner'] = (
                (self.df.loc[mask, 'HHStatus'].isin(['1','2'])) &
                (self.df.loc[mask, 'HHTenureType'] == '1')).astype(int)
            self.logger.info(f"Generated Displaced HHs who own a residential property flag for {self.indicator_name}")
        except Exception as e:
            self.logger.error(f"Error checking Displaced HHs who own a residential property: {e}")
        