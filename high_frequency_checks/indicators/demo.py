import pandas as pd
import numpy as np
import logging
from high_frequency_checks.indicators.base_indicator import BaseIndicator
    
class Demo(BaseIndicator):
    
    flags = {
        'Flag_Demo_Missing': "Missing value(s) in the Demographics Module",
        'Flag_Demo_Erroneous': "Demographics Module has invalid range of values (e.g. household size > 30 or no people in the household)",
        'Flag_Demo_High_HHSize': "The Household Size is very high",
        'Flag_Demo_PLW_Higher_F1259': "Number of PLW exceeds females 12-59",
        'Flag_Demo_Inconsistent_HHSize': "Sum of Males and Females does not match the household size",
        'Flag_Demo_No_Adults': "There are no adults in the household",
    }
        
    def __init__(self, df, base_cols, standard_config, configurable_config, flags):
        super().__init__(df, base_cols, standard_config, configurable_config, flags)
        self.logger = logging.getLogger(__name__)
        self.male_cols = list(self.standard_config.get('male_cols', {}))
        self.female_cols = list(self.standard_config.get('female_cols', {}))
        self.adult_cols = list(self.standard_config.get('adult_cols', {}))
        self.children_cols = list(self.standard_config.get('children_cols', {}))
        self.female1259_cols = list(self.standard_config.get('females1259', {}))
        self.high_hhsize = self.configurable_config.get('high_hhsize')

    def _process_specific(self):
        self.logger.info("Performing specific processing for Demo indicator")
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous'] == 0
        self.calculate_sum_males(mask)
        self.calculate_sum_females(mask)
        self.calculate_sum_m_f(mask)
        self.calculate_sum_adults(mask)
        self.calculate_sum_children(mask)
        self.calculate_sum_f1259(mask)
        self.check_high_hhsize(mask)
        self.check_inconsistent_hhsize(mask)
        self.check_no_adults(mask)
        self.check_plw_higher_f1259(mask)
       
    def calculate_sum_males(self, mask):
        self.logger.info("Calculating total males...")
        try:
            self.df.loc[mask, 'Sum_M'] = self.df.loc[mask, self.male_cols].sum(axis=1)
            self.logger.info("Total males calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating total males: {e}")       

    def calculate_sum_females(self, mask):
        self.logger.info("Calculating total females...")
        try:
            self.df.loc[mask, 'Sum_F'] = self.df.loc[mask, self.female_cols].sum(axis=1)
            self.logger.info("Total females calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating total females: {e}")  
            
    def calculate_sum_m_f(self, mask):
        self.logger.info("Calculating total males and females...")
        try:
            self.df.loc[mask, 'Sum_M_F'] = self.df.loc[mask, 'Sum_M'] + self.df.loc[mask, 'Sum_F']
            self.logger.info("Total males and females calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating total males and females: {e}")  

    def calculate_sum_children(self, mask):
        self.logger.info("Calculating total children...")
        try:
            self.df.loc[mask, 'Sum_Children'] = self.df.loc[mask, self.children_cols].sum(axis=1)
            self.logger.info("Total children calculated successfully")
        except Exception as e:
            self.logger.error(f"Error children total females: {e}")

    def calculate_sum_adults(self, mask):
        self.logger.info("Calculating total adults...")
        try:
            self.df.loc[mask, 'Sum_Adults'] = self.df.loc[mask, self.adult_cols].sum(axis=1)
            self.logger.info("Total adults calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating total adults: {e}") 
            
    def calculate_sum_f1259(self, mask):
        self.logger.info("Calculating total females between 12 and 59...")
        try:
            self.df.loc[mask, 'Sum_F1259'] = self.df.loc[mask, self.female1259_cols].sum(axis=1)
            self.logger.info("Total females between 12 and 59 calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating total females between 12 and 59: {e}")

    def check_high_hhsize(self, mask):
        self.logger.info("Checking for high household size")
        try:
            self.df.loc[mask, 'Flag_Demo_High_HHSize'] = (self.df.loc[mask, 'HHSize'] > self.high_hhsize).astype(int)
            self.logger.info("Generated high household size flag")
        except Exception as e:
            self.logger.error(f"Error checking high household size: {e}")
            
    def check_inconsistent_hhsize(self, mask):
        self.logger.info("Checking for inconsistent household size")
        try:
            self.df.loc[mask, 'Flag_Demo_Inconsistent_HHSize'] = (self.df.loc[mask, 'Sum_M_F'] != self.df.loc[mask, 'HHSize']).astype(int)
            self.logger.info("Generated inconsistent household size flag")
        except Exception as e:
            self.logger.error(f"Error checking inconsistent household size: {e}")

    def check_no_adults(self, mask):
        self.logger.info("Checking for no adults")
        try:
            self.df.loc[mask, 'Flag_Demo_No_Adults'] = (self.df.loc[mask, self.adult_cols].sum(axis=1) == 0).astype(int)
            self.logger.info("Generated no adults flag")
        except Exception as e:
            self.logger.error(f"Error checking no adults: {e}")

    def check_plw_higher_f1259(self, mask):
        self.logger.info("Checking for PLW higher than F1259")
        plw_mask = ~self.df['HHPregLactNb'].isnull()
        combined_mask = plw_mask & mask
        try:
            self.df.loc[combined_mask, 'Flag_Demo_PLW_Higher_F1259'] = (self.df.loc[combined_mask, 'HHPregLactNb'] > self.df.loc[combined_mask, 'Sum_F1259']).astype(int)
            self.logger.info("Generated PLW higher than F1259 flag")
        except Exception as e:
            self.logger.error(f"Error checking PLW higher than F1259: {e}")
