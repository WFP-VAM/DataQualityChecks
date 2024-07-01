import pandas as pd
import numpy as np
from .helpers.base_indicator import BaseIndicator
from .helpers.standard.fexp_7d import fexp_7d_cols
import logging

logname = "logs/HFC.log"

logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

fexp_7d_flags = {
    'Flag_FEXP_7D_Missing_Values': "Missing value(s) in the Food Expenditures 7D Module",
    'Flag_FEXP_7D_Erroneous_Values': "Erroneous value(s) in the Food Expenditures 7D Module",
    'Flag_FEXP_7D_Zero_FEXP': "No Food Purchases/GiftAid/OwnProduction Reported in the last 7 days"
}

class FEXP_7D(BaseIndicator):
"""
    The FEXP_7D class is a subclass of the BaseIndicator class and is responsible for handling the logic related to the Food Expenditures 7D module. It performs the following tasks:
    
    1. Initializes the class with the input DataFrame, low and high erroneous values, and sets up the necessary attributes.
    2. Implements the custom_flag_logic method to handle the custom missing values logic for the FEXP_7D module and calculate the total food expenditures for the last 7 days.
    3. Implements the calculate_indicators method to calculate the monthly food expenditure based on the 7-day food expenditures.
    """
        def __init__(self,
                 df,
                 low_erroneous,
                 high_erroneous):
        
        super().__init__(df,
                         'FEXP_7D',
                         fexp_7d_cols,
                         fexp_7d_flags,
                         exclude_missing_check=fexp_7d_cols)
        
        self.cols = fexp_7d_cols
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous

    def custom_flag_logic(self):
        # Custom flag logic specific to Food Expenditures 7D
        logging.info(f"Custom flag logic for {self.indicator_name}...")
        
        # Custom Missing Values Logic for FEXP_7D
        for col in self.cols:
            base_col = col.replace('_MN', '')
            self.df[f'Flag_{self.indicator_name}_Missing_Values'] = (
                (self.df[base_col] == 1) & self.df[col].isnull()
            ).astype(int)
        
        # Total Food Expenditures 7D is zero
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Missing_Values'] == 0, f'Flag_{self.indicator_name}_Zero_FEXP'] = \
            (self.df['HHExpF_1M'] == 0).astype(int)

    def calculate_indicators(self):
        logging.info(f"Calculating indicators for {self.indicator_name}...")

        # Calculating Monthly Food Expenditure        
        self.df['HHExpF_1M'] = sum(self.df[col] for col in self.cols) / 7 * 30
