import pandas as pd
import numpy as np
from .helpers.base_indicator import BaseIndicator
from .helpers.standard.fexp_7d import fexp_7d_cols


fexp_7d_flags = {
    'Flag_FEXP_7D_Missing_Values': "Missing value(s) in the Food Expenditures 7D Module",
    'Flag_FEXP_7D_Erroneous_Values': "Erroneous value(s) in the Food Expenditures 7D Module",
    'Flag_FEXP_7D_Zero_FEXP': "No Food Purchases/GiftAid/OwnProduction Reported in the last 7 days"
}

class FEXP_7D(BaseIndicator):
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
        print(f"Custom flag logic for {self.indicator_name}...")
        
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
        print(f"Calculating indicators for {self.indicator_name}...")

        # Calculating Monthly Food Expenditure        
        self.df['HHExpF_1M'] = sum(self.df[col] for col in self.cols) / 7 * 30
