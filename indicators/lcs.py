import pandas as pd
import numpy as np
from helpers.base_indicator import BaseIndicator

# Flags related to rCSI
lcs_flags = {
    'Flag_LCS_Missing_Values': "Missing value(s) in the livelihood coping strategies",
    'Flag_LCS_Erroneous_Values': "Erroneous value(s) in the livelihood coping strategies",
    'Flag_LCS_Poor_FCS_and_Zero_rCSI': "The food consumption is poor with no coping (rCSI=0)",
    'Flag_LCS_Acceptable_FCS_and_High_rCSI': "FCS is high and rCSI is high",
    'Flag_LCS_MealAdult_with_No_Children': "Adults reduced their meal intake for children with no children in HH"
}

class LCS(BaseIndicator):
    def __init__(self, df, high_rcsi, low_erroneous, high_erroneous):
        super().__init__(df, 'LCS', lcs_flags)
        self.high_rcsi = high_rcsi
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous
        lcs_cols = [col for col in self.df.columns if 'lcs' in col]

    def custom_flag_logic(self):
        print("Custom flag logic for LCS...")

        # No Coping With Poor Consumption
        fcs_cat_column = 'FCSCat28' if self.high_sugar_oil_consumption else 'FCSCat21'
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_Poor_FCS_and_Zero_rCSI'] = \
        ((self.df[fcs_cat_column] == 'Poor') & (self.df['rCSI'] == 0)).astype(int)
        
        # Acceptable FCS and High rCSI
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_Acceptable_FCS_and_High_rCSI'] = \
        ((self.df[fcs_cat_column] == 'Poor') & (self.df['rCSI'] >  self.high_rcsi)).astype(int)
        
        # Adults Reducing Meals For Children But There are No Children
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_MealAdult_with_No_Children'] = \
        ((self.df['rCSIMealAdult'] > 0) & (self.df['Sum_children'] == 0)).astype(int)

    def calculate_indicators(self):
        print("Calculating rCSI...")
        self.df['rCSI'] = sum(self.df[col] * weight for col, weight in zip(self.cols, self.weights))
        pass
