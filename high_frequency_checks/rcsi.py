import pandas as pd
import numpy as np
import logging
from high_frequency_checks.helpers.base_indicator import BaseIndicator
    
    
class rCSI(BaseIndicator):
"""
    The `rCSI` class is a subclass of `BaseIndicator` and is responsible for processing and calculating the Reduced Coping Strategies Index (rCSI) for a given dataset.
    
    The class has several methods that perform the following tasks:
    - `calculate_rcsi`: Calculates the rCSI based on the provided weights and the values in the dataset.
    - `check_identical_values`: Checks if the values of all reduced coping strategies are identical.
    - `check_poor_fcg_no_coping`: Checks if the food consumption is poor with no reduced coping.
    - `check_acceptable_fcg_high_coping`: Checks if the food consumption is acceptable and the rCSI is high.
    - `check_meal_adult_no_children`: Checks if adults reduced their meal intake for children with no children in the household.
    
    The class also has several flags that are used to indicate the different types of issues that can be found in the dataset.
    """
        
    flags = {
        'Flag_rCSI_Missing': "Missing value(s) in the reduced coping strategies",
        'Flag_rCSI_Erroneous': "Erroneous value(s) in the reduced coping strategies",
        'Flag_rCSI_Identical': "The values of all reduced coping strategies are identical",
        'Flag_rCSI_Poor_FCG_No_Coping': "The food consumption is poor with no reduced coping",
        'Flag_rCSI_Acceptable_FCG_High_Coping': "The food consumption is acceptable and rCSI is high",
        'Flag_rCSI_MealAdult_No_Children': "Adults reduced their meal intake for children with no children in HH"
    }
        
    def __init__(self, df, base_cols, review_cols, standard_config, configurable_config, flags):
        super().__init__(df, base_cols, review_cols, standard_config, configurable_config, flags)
        self.logger = logging.getLogger(__name__)
        self.weights = self.standard_config.get('weights', {})
        self.high_sugar_oil_consumption = self.configurable_config.get('high_sugar_oil_consumption')
        self.high_rcsi = self.configurable_config.get('high_rcsi')
        
    def _process_specific(self):
        self.logger.info("Performing specific processing for rCSI indicator")
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous'] == 0
        self.check_identical_values(mask)
        self.calculate_rcsi(mask)
        self.check_poor_fcg_no_coping(mask)
        self.check_acceptable_fcg_high_coping(mask)
        self.check_meal_adult_no_children(mask)
        
    def calculate_rcsi(self, mask):
        self.logger.info("Calculating rCSI")
        try:
            self.df.loc[mask, 'rCSI'] = sum(self.df.loc[mask, col] * weight for col, weight in self.weights.items())
            self.logger.info("rCSI calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating rCSI: {e}")
            
    def check_identical_values(self, mask):
        self.logger.info(f"Checking for identical values for {self.indicator_name}")
        try:
            self.df.loc[mask, f'Flag_{self.indicator_name}_Identical'] = ((self.df.loc[mask, self.cols].nunique(axis=1) == 1) & (self.df.loc[mask, self.cols].sum(axis=1) != 0)).astype(int)
            self.logger.info(f"Generated identical values flag for {self.indicator_name}")
        except Exception as e:
            self.logger.error(f"Error checking identical values for {self.indicator_name}: {e}")

    def check_poor_fcg_no_coping(self, mask):
        self.logger.info("Checking for Poor FCG with No Reduced Coping")
        try:
            fcs_cat_column = 'FCSCat28' if self.high_sugar_oil_consumption else 'FCSCat21'
            self.df.loc[mask, 'Flag_rCSI_Poor_FCG_No_Coping'] = \
            ((self.df.loc[mask, fcs_cat_column] == 'Poor') & (self.df.loc[mask, 'rCSI'] == 0)).astype(int)
            self.logger.info("Generated Poor FCG with No Reduced Coping flag")
        except Exception as e:
            self.logger.error(f"Error checking Poor FCG with No Reduced Coping: {e}")

    def check_acceptable_fcg_high_coping(self, mask):
        self.logger.info("Checking for Acceptable FCG with High Reduced Coping")
        try:
            fcs_cat_column = 'FCSCat28' if self.high_sugar_oil_consumption else 'FCSCat21'
            self.df.loc[mask, 'Flag_rCSI_Acceptable_FCG_High_Coping'] = \
            ((self.df.loc[mask, fcs_cat_column] == 'Acceptable') & (self.df.loc[mask, 'rCSI'] > self.high_rcsi)).astype(int)
            self.logger.info("Generated Acceptable FCG with High Reduced Coping flag")
        except Exception as e:
            self.logger.error(f"Error checking Acceptable FCG with High Reduced Coping: {e}")

    def check_meal_adult_no_children(self, mask):
        self.logger.info("Checking for Adults Reducing Meals with No Children")
        try:
            # Create masks to handle NaN values
            not_nan_rCSI = ~self.df['rCSIMealAdult'].isnull()
            not_nan_children = ~self.df['Sum_Children'].isnull()

            # Apply conditions with NaN handling
            self.df.loc[mask & not_nan_rCSI & not_nan_children, 'Flag_rCSI_MealAdult_No_Children'] = \
                ((self.df.loc[mask & not_nan_rCSI & not_nan_children, 'rCSIMealAdult'] > 0) &
                (self.df.loc[mask & not_nan_rCSI & not_nan_children, 'Sum_Children'] == 0)).astype(int)

            # Handle NaN values appropriately (setting flag to NaN or default value)
            self.df.loc[mask & (~not_nan_rCSI | ~not_nan_children), 'Flag_rCSI_MealAdult_No_Children'] = np.nan
            
            self.logger.info("Generated Adults Reducing Meals with No Children flag")
        except Exception as e:
            self.logger.error(f"Error checking Adults Reducing Meals with No Children: {e}")

