import pandas as pd
import numpy as np
from .helpers.base_indicator import BaseIndicator
from .helpers.standard.lcs import lcs_stress_cols, lcs_crisis_cols, lcs_em_cols, lcs_children_cols, lcs_non_exhaustive_cols, lcs_options
import logging

logname = "logs/HFC.log"

logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


class LCS(BaseIndicator):
    
    lcs_flags = {
    'Flag_LCS_Missing_Values': "Missing value(s) in the livelihood coping strategies",
    'Flag_LCS_Erroneous_Values': "Erroneous value(s) in the livelihood coping strategies",
    'Flag_LCS_ChildrenStrategies_with_No_Children': "HH Applied strategies related to children with no children",
    'Flag_LCS_Three_or_More_NA': "Three or more livelihood coping strategies reported as NA",
    'Flag_LCS_NonExhaustive_Strategies_NA': "HH Reported activities that can't be exhausted as exhausted or Not Applicable"
}
    
    def __init__(self,
                 df,
                 low_erroneous,
                 high_erroneous):
        
        self.df = df
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous
        self.lcs_stress_cols = [col for col in lcs_stress_cols if col in self.df.columns]
        self.lcs_crisis_cols = [col for col in lcs_crisis_cols if col in self.df.columns]
        self.lcs_em_cols = [col for col in lcs_em_cols if col in self.df.columns]
        self.lcs_cols = self.lcs_stress_cols + self.lcs_crisis_cols + self.lcs_em_cols
        self.lcs_options = lcs_options
        
        super().__init__(df,
                    'LCS',
                    self.lcs_cols,
                    LCS.lcs_flags,
                    exclude_erroneous_check=self.lcs_cols)

        
    def custom_flag_logic(self):
        logging.info("Custom flag logic for LCS...")

        # Custom Erroneous value Logic for LCS Columns
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Missing_Values'] == 0, f'Flag_{self.indicator_name}_Erroneous_Values'] = (
            ~self.df[self.lcs_cols].isin(self.lcs_options).all(axis=1)
            ).astype(int)
        
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0
        
        # HH Applying livelihood strategies related to children But There are No Children
        children_cols_present = [col for col in lcs_children_cols if col in self.df.columns]
        if children_cols_present:
            self.df.loc[mask, f'Flag_{self.indicator_name}_ChildrenStrategies_with_No_Children'] = (
                (self.df['Sum_children'] == 0) & 
                self.df[children_cols_present].isin([20, 30]).any(axis=1)
            ).astype(int)
        else:
            self.df.loc[mask, f'Flag_{self.indicator_name}_ChildrenStrategies_with_No_Children'] = 0
            
        # Flag for three or More N/A in Strategies
        self.df.loc[mask, f'Flag_{self.indicator_name}_Three_or_More_NA'] = (
            (self.df[self.lcs_cols] == 9999).sum(axis=1) >= 3
        ).astype(int)
        
        # Flag if specific strategies that can't be exhausted or NA (Begging, Borrowing Money, and Illegal activities) are reported as exhausted or not applicable
        non_exhaustive_cols_present = [col for col in lcs_non_exhaustive_cols if col in self.df.columns]
        if non_exhaustive_cols_present:
            self.df.loc[mask, f'Flag_{self.indicator_name}_NonExhaustive_Strategies_NA'] = (
                self.df[non_exhaustive_cols_present].isin([30, 9999]).any(axis=1)
            ).astype(int)
        else:
            self.df.loc[mask, f'Flag_{self.indicator_name}_NonExhaustive_Strategies_NA'] = 0
        
    def calculate_indicators(self):
        pass
    