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
    'Flag_rCSI_Abnormal_Identical': "The values of all reduced coping strategies is identical",
    'Flag_rCSI': "One or more rCSI flag(s) triggered"
}

class rCSI(BaseIndicator):
    def __init__(self, df, low_erroneous, high_erroneous):
        super().__init__(df, 'rCSI', rcsi_cols, rcsi_flags, rcsi_weights)
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous

    def custom_flag_logic(self):
        print("Custom flag logic for rCSI...")
        # Identical Values
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_Abnormal_Identical'] = \
            (self.df[self.cols].nunique(axis=1) == 1).astype(int)

    def calculate_rCSI(self):
        print("Calculating rCSI...")
        self.df['rCSI'] = sum(self.df[col] * weight for col, weight in zip(self.cols, self.weights))
        pass
