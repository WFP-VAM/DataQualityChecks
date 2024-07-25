import pandas as pd
import numpy as np
import logging
from high_frequency_checks.helpers.base_indicator import BaseIndicator

class FCS(BaseIndicator):
    """
    The `FCS` class is a subclass of `BaseIndicator` and is responsible for processing and calculating the Food Consumption Score (FCS) indicator.

    The class has several flags that are used to indicate different issues with the FCS data, such as missing values, erroneous values, identical values, low staple consumption, low FCS, and high FCS.

    The `__init__` method initializes the class with the necessary data and configuration parameters, including the weights for calculating the FCS and various thresholds for the different flags.

    The `_process_specific` method performs the specific processing for the FCS indicator, including checking for identical values, calculating the FCS and Food Consumption Group (FCG), and checking for low staple consumption, low FCS, and high FCS.

    The `calculate_fcs` method calculates the FCS by multiplying the consumption values for each food group by the corresponding weights and summing the results.

    The `calculate_fcg` method calculates the FCG by categorizing the FCS values into "Poor", "Borderline", and "Acceptable" based on the configured thresholds.

    The `check_identical_values`, `check_low_staple`, `check_low_fcs`, and `check_high_fcs` methods generate flags for the corresponding issues with the FCS data.
    """
                
    flags = {
        'Flag_FCS_Missing': "Missing value(s) in the consumption of the 8 main food groups",
        'Flag_FCS_Erroneous': "Invalid value(s) in the consumption of the 8 main food groups i.e. food group <0 or >7",
        'Flag_FCS_Identical': "The consumption of all 8 main food groups is identical",
        'Flag_FCS_Low_Staple': "Low staple consumption",
        'Flag_FCS_Low_FCS': "Low FCS",
        'Flag_FCS_High_FCS': "High FCS",
    }
        
    def __init__(self, df, base_cols, standard_config, configurable_config, flags):
        super().__init__(df, base_cols, standard_config, configurable_config, flags)
        self.logger = logging.getLogger(__name__)
        self.weights = self.standard_config.get('weights', {})
        self.high_sugar_oil_consumption = self.configurable_config.get('high_sugar_oil_consumption')
        self.low_fcs = self.configurable_config.get('low_fcs')
        self.high_fcs = self.configurable_config.get('high_fcs')
        self.low_staple = self.configurable_config.get('low_staple')
        
    def _process_specific(self):
        self.logger.info("Performing specific processing for FCS indicator")
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous'] == 0
        self.check_identical_values(mask)
        self.calculate_fcs(mask)
        self.calculate_fcg(mask)
        self.check_low_staple(mask)
        self.check_low_fcs(mask)
        self.check_high_fcs(mask)
        
    def calculate_fcs(self, mask):
        self.logger.info("Calculating FCS")
        try:
            self.df.loc[mask, 'FCS'] = sum(self.df[col] * weight for col, weight in self.weights.items())
            self.logger.info("FCS calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating FCS: {e}")

    def calculate_fcg(self, mask):
        self.logger.info("Calculating FCG")
        try:
            if self.high_sugar_oil_consumption == 1:
                self.df.loc[mask, 'FCSCat28'] = pd.cut(self.df.loc[mask, 'FCS'], bins=[0, 28.5, 42.5, float('inf')], labels=['Poor', 'Borderline', 'Acceptable'], right=False)
            else:
                self.df.loc[mask, 'FCSCat21'] = pd.cut(self.df.loc[mask, 'FCS'], bins=[0, 21.5, 35.5, float('inf')], labels=['Poor', 'Borderline', 'Acceptable'], right=False)
            self.logger.info("FCG calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating FCG: {e}")
            
    def check_identical_values(self, mask):
        self.logger.info(f"Checking for identical values for {self.indicator_name}")
        try:
            self.df.loc[mask, f'Flag_{self.indicator_name}_Identical'] = (self.df.loc[mask, self.cols].nunique(axis=1) == 1).astype(int)
            self.logger.info(f"Generated identical values flag for {self.indicator_name}")
        except Exception as e:
            self.logger.error(f"Error checking identical values for {self.indicator_name}: {e}")

    def check_low_staple(self, mask):
        self.logger.info(f"Checking for low staple consumption for {self.indicator_name}")
        try:
            self.df.loc[mask, f'Flag_FCS_Low_Staple'] = (self.df.loc[mask, 'FCSStap'] < self.low_staple).astype(int)
            self.logger.info(f"Generated low staple consumption flag for {self.indicator_name}")      
        except Exception as e:
            self.logger.error(f"Error checking low staple consumption for {self.indicator_name}: {e}") 
    
    def check_low_fcs(self, mask):
        self.logger.info("Checking for low FCS")
        try:
            self.df.loc[mask, f'Flag_FCS_Low_FCS'] = (self.df.loc[mask, 'FCS'] < self.low_fcs).astype(int)
            self.logger.info(f"Generated low FCS flag for {self.indicator_name}")
        except Exception as e:
            self.logger.error(f"Error checking low FCS: {e}")

    def check_high_fcs(self, mask):
        self.logger.info("Checking for high FCS")
        try:
            self.df.loc[mask, f'Flag_FCS_High_FCS'] = (self.df.loc[mask, 'FCS'] > self.high_fcs).astype(int)
            self.logger.info(f"Generated high FCS flag for {self.indicator_name}")
        except Exception as e:
            self.logger.error(f"Error checking high FCS: {e}")
