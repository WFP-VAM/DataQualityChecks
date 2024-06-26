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
    def __init__(self, df, low_erroneous, high_erroneous):
        super().__init__(df, 'HDDS', hdds_cols, hdds_flags)
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous
        
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
        
    def calculate_hdds(self):
        print("Calculating HDDS...")

        # self.df['HDDS'] = 0

        self.df['HDDS'] = (self.df['HDDSStapCer'] + self.df['HDDSStapRoot'] + self.df['HDDSVeg'] + self.df['HDDSFruit'] +
                        self.df['HDDSPrMeatF'] + self.df['HDDSPrMeatO'] + self.df['HDDSPrFish'] + self.df['HDDSPulse'] +
                        self.df['HDDSDairy'] + self.df['HDDSFat'] + self.df['HDDSSugar'] + self.df['HDDSCond'])

        # Replace NaN values with 0 if present
        self.df['HDDS'] = self.df['HDDS'].fillna(0)

        # Create HDDS categories
        conditions = [
            (self.df['HDDS'] >= 0) & (self.df['HDDS'] <= 2),
            (self.df['HDDS'] >= 3) & (self.df['HDDS'] <= 4),
            (self.df['HDDS'] >= 5)
        ]
        values = ['0-2 food groups (phase 4 to 5)', '3-4 food groups (phase 3)', '5-12 food groups (phase 1 to 2)']
        self.df['HDDSCat_IPC'] = pd.np.select(conditions, values)

        
    # Create flag columns in the DataFrame
    def custom_flag_logic(self):
        # for key in self.column_pairs.keys():
        #     self.df[f"Flag_{self.indicator_name}{key}_mismatch"] = False

        for key, cols in self.column_pairs.items():
            fcs_col, *hdds_cols = cols
            fcs_values = self.df[fcs_col]
            hdds_values = [self.df[col].fillna(0) for col in hdds_cols]  # Replace NaN with 0

            # Check for mismatches row-wise
            mismatch_condition = (fcs_values == 7) & (np.any(np.array(hdds_values) == 0, axis=0))
            flag_column_name = f"Flag_{self.indicator_name}{key}_mismatch"
            self.df[flag_column_name] = mismatch_condition

        return self.df