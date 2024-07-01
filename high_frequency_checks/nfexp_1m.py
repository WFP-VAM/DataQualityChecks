import pandas as pd
import numpy as np
from .helpers.base_indicator import BaseIndicator
from .helpers.standard.nfexp_1m import nfexp_1m_cols
import logging

logname = "logs/HFC.log"

logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

nfexp_1m_flags = {
    'Flag_NFEXP_1M_Missing_Values': "Missing value(s) in the Non-Food Expenditures 1M Module",
    'Flag_NFEXP_1M_Erroneous_Values': "Erroneous value(s) in the Non-Food Expenditures 1M Module",
}

class NFEXP_1M(BaseIndicator):
"""
    Implements the NFEXP_1M (Non-Food Expenditures 1M) indicator, which calculates the monthly non-food expenditure for a given dataset.
    
    The NFEXP_1M class inherits from the BaseIndicator class and implements the custom flag logic and indicator calculation for the Non-Food Expenditures 1M module.
    
    The class takes a DataFrame, low and high erroneous values as input, and calculates the monthly non-food expenditure by summing the relevant columns from the input DataFrame.
    """
        def __init__(self,
                 df,
                 low_erroneous,
                 high_erroneous):
        
        super().__init__(df,
                         'NFEXP_1M',
                         nfexp_1m_cols,
                         nfexp_1m_flags,
                         exclude_missing_check=nfexp_1m_cols)
        
        self.cols = nfexp_1m_cols
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous

    def custom_flag_logic(self):
        # Custom flag logic specific to Non-Food Expenditures 1M
        logging.info(f"Custom flag logic for {self.indicator_name}...")
        
        # Custom Missing Values Logic for NFEXP_1M
        for col in self.cols:
            base_col = col.replace('_MN', '')
            self.df[f'Flag_{self.indicator_name}_Missing_Values'] = (
                (self.df[base_col] == 1) & self.df[col].isnull()
            ).astype(int)

    def calculate_indicators(self):
        logging.info(f"Calculating indicators for {self.indicator_name}...")
        
        # Calculating Monthly Non-Food Expenditure 1M
        self.df['HHExpNF_1M_1M'] = sum(self.df[col] for col in self.cols)
