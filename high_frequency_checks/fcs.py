import pandas as pd
import numpy as np
from .helpers.base_indicator import BaseIndicator
from .helpers.standard.fcs import fcs_cols, fcs_weights


class FCS(BaseIndicator):
    
    flags = {
        'Flag_FCS_Missing_Values': "Missing value(s) in the consumption of the 8 main food groups",
        'Flag_FCS_Erroneous_Values': "Erroneous value(s) (negative or above 7) in the consumption of the 8 main food groups",
        'Flag_FCS_Abnormal_Identical': "The consumption of all 8 main food groups is identical",
        'Flag_FCS_Low_Staple': "Low staple consumption (below 4)",
        'Flag_FCS_Low_FCS': "Low FCS",
        'Flag_FCS_High_FCS': "High FCS",
}
    def __init__(self,
                 df,
                 low_fcs,
                 high_fcs,
                 low_erroneous,
                 high_erroneous,
                 high_sugar_oil_consumption):
        
        super().__init__(df, 
                         'FCS',
                         fcs_cols,
                         FCS.flags,
                         )
        
        self.cols = fcs_cols
        self.weights = fcs_weights
        self.low_fcs = low_fcs
        self.high_fcs = high_fcs
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous
        self.high_sugar_oil_consumption = high_sugar_oil_consumption

    def calculate_indicators(self):
        print("Calculating FCS...")
        self.df['FCS'] = sum(self.df[col] * weight for col, weight in zip(self.cols, self.weights))
        self.calculate_fcg()

    def custom_flag_logic(self):
        print("Custom flag logic for FCS...")
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0
        
        # Identical Values
        self.df.loc[mask, 'Flag_FCS_Abnormal_Identical'] = (self.df[self.cols].nunique(axis=1) == 1).astype(int)

        # Low Staple Consumption
        self.df.loc[mask, f'Flag_FCS_Low_Staple'] = (self.df['FCSStap'] < 4).astype(int)

        # Low FCS
        self.df.loc[mask, f'Flag_FCS_Low_FCS'] = (self.df['FCS'] < self.low_fcs).astype(int)

        # High FCS
        self.df.loc[mask, f'Flag_FCS_High_FCS'] = (self.df['FCS'] > self.high_fcs).astype(int)

    def calculate_fcg(self):
        print("Calculating FCG...")
        if self.high_sugar_oil_consumption:
            self.df['FCSCat28'] = pd.cut(self.df['FCS'], bins=[0, 28.5, 42.5, float('inf')], labels=['Poor', 'Borderline', 'Acceptable'], right=False)
        else:
            self.df['FCSCat21'] = pd.cut(self.df['FCS'], bins=[0, 21.5, 35.5, float('inf')], labels=['Poor', 'Borderline', 'Acceptable'], right=False)
