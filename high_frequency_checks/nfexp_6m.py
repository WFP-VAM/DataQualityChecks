import pandas as pd
import numpy as np
from .helpers.base_indicator import BaseIndicator
from .helpers.standard.nfexp_6m import nfexp_6m_cols
import logging

logname = "logs/HFC.log"

logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

nfexp_6m_flags = {
    'Flag_NFEXP_6M_Missing_Values': "Missing value(s) in the Non-Food Expenditures 6M Module",
    'Flag_NFEXP_6M_Erroneous_Values': "Erroneous value(s) in the Non-Food Expenditures 6M Module",
}

class NFEXP_6M(BaseIndicator):
"""
    Calculates the Non-Food Expenditures 6M indicators for a given DataFrame.
    
    The `NFEXP_6M` class is a subclass of `BaseIndicator` and is responsible for calculating the Non-Food Expenditures 6M indicators. It takes a DataFrame, low and high erroneous values, and performs the following tasks:
    
    1. Initializes the base indicator properties using the `BaseIndicator` class.
    2. Implements custom flag logic to identify missing values in the Non-Food Expenditures 6M module.
    3. Calculates the monthly Non-Food Expenditures 6M and the total monthly expenditures.
    
    The class uses the `nfexp_6m_cols` and `nfexp_6m_flags` constants defined in the `helpers.standard.nfexp_6m` module.
    """
        def __init__(self, 
                 df,
                 low_erroneous,
                 high_erroneous):
        
        super().__init__(df,
                         'NFEXP_6M',
                         nfexp_6m_cols,
                         nfexp_6m_flags,
                         exclude_missing_check=nfexp_6m_cols)
        
        self.cols = nfexp_6m_cols
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous

    def custom_flag_logic(self):
        # Custom flag logic specific to Non-Food Expenditures 6M
        logging.info(f"Custom flag logic for {self.indicator_name}...")
        
        # Custom Missing Values Logic for NFEXP_1M
        for col in self.cols:
            base_col = col.replace('_MN', '')
            self.df[f'Flag_{self.indicator_name}_Missing_Values'] = (
                (self.df[base_col] == 1) & self.df[col].isnull()
            ).astype(int)

    def calculate_indicators(self):
        logging.info(f"Calculating indicators for {self.indicator_name}...")
        
        # Calculating Monthly Non-Food Expenditures 6M        
        self.df['HHExpNF_6M_1M'] = sum(self.df[col] for col in self.cols) / 6
        
        # Calculating Total Monthly Expenditures
        self.df['HHExp_1M'] = self.df['HHExpF_1M'] + self.df['HHExpNF_1M_1M'] + self.df['HHExpNF_6M_1M']
