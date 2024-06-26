import pandas as pd
import numpy as np
from helpers.base_indicator import BaseIndicator

# Columns of food groups related to HDDS
hdds_cols = ['HDDSStapCer', 'HDDSStapRoot', 'HDDSPulse', 'HDDSDairy', 'HDDSPrMeatF', 'HDDSPrMeatO', 'HDDSPrFish', 'HDDSPrEggs', 'HDDSVeg', 'HDDSFruit', 'HDDSFat', 'HDDSSugar', 'HDDSCond']

# Flags related to HDDS
hdds_flags = {
    'Flag_HDDS_Missing_Values': "Missing value(s) in the consumption of the food groups",
    'Flag_HDDS_Erroneous_Values': "Erroneous value(s) (not 1 or 0)",
    'Flag_HDDS_Identical_Values': "0 values across the food groups",
    'Flag_HDDS_FCSStap_mismatch': "Mismatch between FCSStap and HDDSStapCer/HDDSStapRoot",
    'Flag_HDDS_FCSPulse_mismatch': "Mismatch between FCSPulse and HDDSPulse",
    'Flag_HDDS_FCSDairy_mismatch': "Mismatch between FCSDairy and HDDSDairy",
    'Flag_HDDS_FCSPr_mismatch': "Mismatch between FCSPr and HDDSPrMeatF/HDDSPrMeatO/HDDSPrFish/HDDSPrEggs",
    'Flag_HDDS_FCSVeg_mismatch': "Mismatch between FCSVeg and HDDSVeg",
    'Flag_HDDS_FCSFruit_mismatch': "Mismatch between FCSFruit and HDDSFruit",
    'Flag_HDDS_FCSFat_mismatch': "Mismatch between FCSFat and HDDSFat",
    'Flag_HDDS_FCSSugar_mismatch': "Mismatch between FCSSugar and HDDSSugar",
    'Flag_HDDS_FCSCond_mismatch': "Mismatch between FCSCond and HDDSCond"
}

class HDDS(BaseIndicator):
    def __init__(self, df, low_erroneous, high_erroneous):
        super().__init__(df, 'HDDS', hdds_cols, hdds_flags)
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous
        self.hdds_cols = hdds_cols  # Make hdds_cols a class attribute

        self.FCS_HDDS_pairs = {
            "FCSStap": ("HDDSStapCer", "HDDSStapRoot"),
            "FCSPulse": ("HDDSPulse"),
            "FCSDairy": ("HDDSDairy"),
            "FCSPr": ("HDDSPrMeatF", "HDDSPrMeatO", "HDDSPrFish", "HDDSPrEggs"),
            "FCSVeg": ("HDDSVeg"),
            "FCSFruit": ("HDDSFruit"),
            "FCSFat": ("HDDSFat"),
            "FCSSugar": ("HDDSSugar"),
            "FCSCond": ("HDDSCond")
        }
        
    def calculate_indicators(self):
        print("Calculating HDDS...")

        self.df['HDDS'] = (self.df['HDDSStapCer'] + self.df['HDDSStapRoot'] + self.df['HDDSVeg'] + self.df['HDDSFruit'] +
                        self.df['HDDSPrMeatF'] + self.df['HDDSPrMeatO'] + self.df['HDDSPrFish'] + self.df['HDDSPulse'] +
                        self.df['HDDSDairy'] + self.df['HDDSFat'] + self.df['HDDSSugar'] + self.df['HDDSCond'])

        # Replace NaN values with 0 if present
        self.df['HDDS'] = self.df['HDDS'].fillna(0)

        # Create HDDS categories
        bins = [0, 2, 4, self.df['HDDS'].max() + 1]  # Define the bin edges
        labels = ['0-2 food groups (phase 4 to 5)', '3-4 food groups (phase 3)', '5-12 food groups (phase 1 to 2)']

        self.df['HDDSCat_IPC'] = pd.cut(self.df['HDDS'], bins=bins, labels=labels, include_lowest=True)

    def custom_flag_logic(self):

        for col in hdds_flags.keys():
            self.df[col] = 0

        # Identical Values (All 0's)
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_Identical_Values'] = \
        (self.df[self.hdds_cols].sum(axis=1) == 0).astype(int)

        # Check mismatch on Staple foods
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_FCSStap_mismatch'] = \
        ((self.df["FCSStap"] == 7) & ((self.df['HDDSStapCer'] == 0) & (self.df['HDDSStapRoot'] == 0))).astype(int)

        # Check mismatch on Pulses
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_FCSPulse_mismatch'] = \
        ((self.df["FCSPulse"] == 7) & (self.df['HDDSPulse'] == 0)).astype(int)

        # Check mismatch on Dairy
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_FCSDairy_mismatch'] = \
        ((self.df["FCSDairy"] == 7) & (self.df['HDDSDairy'] == 0)).astype(int)

        # Check mismatch on Proteins
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_FCSPr_mismatch'] = \
        ((self.df["FCSPr"] == 7) & ((self.df['HDDSPrMeatF'] == 0) & (self.df['HDDSPrMeatO'] == 0) & (self.df['HDDSPrFish'] == 0) & (self.df['HDDSPrEggs'] == 0))).astype(int)

        # Check mismatch on Vegetables
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_FCSVeg_mismatch'] = \
        ((self.df["FCSVeg"] == 7) & (self.df['HDDSVeg'] == 0)).astype(int)

        # Check mismatch on Fruits
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_FCSFruit_mismatch'] = \
        ((self.df["FCSFruit"] == 7) & (self.df['HDDSFruit'] == 0)).astype(int)

        # Check mismatch on Fats
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_FCSFat_mismatch'] = \
        ((self.df["FCSFat"] == 7) & (self.df['HDDSFat'] == 0)).astype(int)

        # Check mismatch on Sugar
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_FCSSugar_mismatch'] = \
        ((self.df["FCSSugar"] == 7) & (self.df['HDDSSugar'] == 0)).astype(int)

        # Check mismatch on Condiments
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_FCSCond_mismatch'] = \
        ((self.df["FCSCond"] == 7) & (self.df['HDDSCond'] == 0)).astype(int)

    def custom_flag_logic_old(self):
        for col in hdds_flags.keys():
            self.df[col] = 0

        # Identical Values (All 0's)
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_Identical_Values'] = \
        (self.df[self.hdds_cols].sum(axis=1) == 0).astype(int)

        # Check mismatches between FCS and HDDS columns
        for fcs_col, hdds_cols in self.FCS_HDDS_pairs.items():
            if isinstance(hdds_cols, str):
                hdds_cols = [hdds_cols]

            mismatch_condition = ((self.df[fcs_col] == 7) & (self.df[list(hdds_cols)].sum(axis=1) == 0))
            flag_name = f'Flag_HDDS_{fcs_col}_mismatch'
            self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, flag_name] = mismatch_condition.astype(int)
        
        # Compare flags for each row
        flags_equal = self.df[hdds_flags.keys()].apply(lambda row: row.eq(self.df[hdds_flags.keys()].shift(1)), axis=1).all(axis=1)
        print(f"Number of rows where flags are different: {(~flags_equal).sum()}")
