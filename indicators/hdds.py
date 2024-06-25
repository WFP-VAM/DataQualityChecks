import pandas as pd
import numpy as np
from helpers.base_indicator import BaseIndicator

# Columns of food groups related to HDDS
hdds_cols = ['HDDSStapCer', 'HDDSStapRoot', 'HDDSPulse', 'HDDSDairy', 'HDDSPrMeatF', 'HDDSPrMeatO', 'HDDSPrFish', 'HDDSPrEggs', 'HDDSVeg', 'HDDSFruit', 'HDDSFat', 'HDDSSugar', 'HDDSCond']

# Flags related to HDDS
hdds_flags = {
    'Flag_HDDS_Missing_Values': "Missing value(s) in the consumption of the food groups",
    'Flag_HDDS_Erroneous_Values': "Erroneous value(s) (negative or above 7)",
    'Flag_HDDS_Stap_mismatch': "Mismatch between FCSStap and HDDSStapCer/HDDSStapRoot",
    'Flag_HDDS_Pulse_mismatch': "Mismatch between FCSPulse and HDDSPulse",
    'Flag_HDDS_Dairy_mismatch': "Mismatch between FCSDairy and HDDSDairy",
    'Flag_HDDS_Pr_mismatch': "Mismatch between FCSPr and HDDSPrMeatF/HDDSPrMeatO/HDDSPrFish/HDDSPrEggs",
    'Flag_HDDS_Veg_mismatch': "Mismatch between FCSVeg and HDDSVeg",
    'Flag_HDDS_Fruit_mismatch': "Mismatch between FCSFruit and HDDSFruit",
    'Flag_HDDS_Fat_mismatch': "Mismatch between FCSFat and HDDSFat",
    'Flag_HDDS_Sugar_mismatch': "Mismatch between FCSSugar and HDDSSugar",
    'Flag_HDDS_Cond_mismatch': "Mismatch between FCSCond and HDDSCond"
}

class HDDS(BaseIndicator):
    def __init__(self, df):
        super().__init__(df, 'HDDS', hdds_cols, hdds_flags)
        self.column_pairs = {
            "Stap": ("FCSStap", "HDDSStapCer", "HDDSStapRoot"),
            "Pulse": ("FCSPulse", "HDDSPulse"),
            "Dairy": ("FCSDairy", "HDDSDairy"),
            "Pr": ("FCSPr", "HDDSPrMeatF", "HDDSPrMeatO", "HDDSPrFish", "HDDSPrEggs"),
            "Veg": ("FCSVeg", "HDDSVeg"),
            "Fruit": ("FCSFruit", "HDDSFruit"),
            "Fat": ("FCSFat", "HDDSFat"),
            "Sugar": ("FCSSugar", "HDDSSugar"),
            "Cond": ("FCSCond", "HDDSCond")
        }

        # Create flag columns in the DataFrame
        for key in self.column_pairs.keys():
            self.df[f"Flag_{self.indicator_name}{key}_mismatch"] = False

    def custom_flag_logic(self):
        pass
        # for key, cols in self.column_pairs.items():
        #     fcs_col, *hdds_cols = cols
        #     fcs_values = self.df[fcs_col]
        #     hdds_values = [self.df[col].fillna(0) for col in hdds_cols]  # Replace NaN with 0

        #     # Check for mismatches row-wise
        #     mismatch_condition = (fcs_values == 7) & (np.any(np.array(hdds_values) == 0, axis=0))
        #     flag_column_name = f"Flag_{self.indicator_name}{key}_mismatch"
        #     self.df[flag_column_name] = mismatch_condition

        # return self.df

#%% Additional code

    # def calculate_fcg(self):
    #     print("Calculating FCG...")
    #     if self.high_sugar_oil_consumption:
    #         self.df['FCSCat28'] = pd.cut(self.df['FCS'], bins=[0, 28.5, 42.5, float('inf')], labels=['Poor', 'Borderline', 'Acceptable'], right=False)
    #     else:
    #         self.df['FCSCat21'] = pd.cut(self.df['FCS'], bins=[0, 21.5, 35.5, float('inf')], labels=['Poor', 'Borderline', 'Acceptable'], right=False)


#%% FCS Code 
# def custom_flag_logic(self):
    #     print("Custom flag logic for FCS...")
    #     # Identical Values
    #     self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_Abnormal_Identical'] = \
    #         (self.df[self.cols].nunique(axis=1) == 1).astype(int)

    #     # Low Staple Consumption
    #     self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_Low_Staple'] = \
    #         (self.df['FCSStap'] < 4).astype(int)

    #     # Low FCS
    #     self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_Low_FCS'] = \
    #         (self.df['FCS'] < self.low_fcs).astype(int)

    #     # High FCS
    #     self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_High_FCS'] = \
    #         (self.df['FCS'] > self.high_fcs).astype(int)
        
    # def custom_flag_logic(self):
    # if household has consumped staples for 0 days in FCS but has not consummed staples in the last 24hrs