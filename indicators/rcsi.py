import pandas as pd
import numpy as np
from helpers.base_indicator import BaseIndicator

# Columns of food groups related to rCSI
rcsi_cols = ['rCSILessQlty',
            'rCSIBorrow',
            'rCSIMealSize',
            'rCSIMealAdult',
            'rCSIMealNb']

# Weights of coping strategies related to rCSI
rcsi_weights = [1, 
                2,
                1,
                3,
                1]

# Flags related to rCSI
rcsi_flags = {
    'Flag_rCSI_Missing_Values': "Missing value(s) in the reduced coping strategies",
    'Flag_rCSI_Erroneous_Values': "Erroneous value(s) (negative or above 7) in the reduced coping strategies",
    'Flag_rCSI_Abnormal_Identical': "The values of all reduced coping strategies are identical",
    'Flag_rCSI_Poor_FCS_and_Zero_rCSI': "The food consumption is poor with no coping (rCSI=0)",
    'Flag_rCSI_Acceptable_FCS_and_High_rCSI': "FCS is high and rCSI is high",
}

class rCSI(BaseIndicator):
    def __init__(self, df, high_rcsi, low_erroneous, high_erroneous, high_sugar_oil_consumption):
        super().__init__(df, 'rCSI', rcsi_cols, rcsi_flags, rcsi_weights)
        self.high_rcsi = high_rcsi
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous
        self.high_sugar_oil_consumption = high_sugar_oil_consumption

    def custom_flag_logic(self):
        print("Custom flag logic for rCSI...")
        
        # Identical Values (Except for 0's)
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_Abnormal_Identical'] = \
        ((self.df[self.cols].nunique(axis=1) == 1) & (self.df[self.cols].sum(axis=1) != 0)).astype(int)

        
        # No Coping With Poor Consumption
        fcs_cat_column = 'FCSCat28' if self.high_sugar_oil_consumption else 'FCSCat21'
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_Poor_FCS_and_Zero_rCSI'] = \
        ((self.df[fcs_cat_column] == 'Poor') & (self.df['rCSI'] == 0)).astype(int)
        
        # Acceptable FCS and High rCSI
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_Acceptable_FCS_and_High_rCSI'] = \
        ((self.df[fcs_cat_column] == 'Poor') & (self.df['rCSI'] >  self.high_rcsi)).astype(int)

    def calculate_indicators(self):
        print("Calculating rCSI...")
        self.df['rCSI'] = sum(self.df[col] * weight for col, weight in zip(self.cols, self.weights))
        pass
