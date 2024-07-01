import pandas as pd
import numpy as np
from .helpers.base_indicator import BaseIndicator

# Columns of food groups related to HDDS
hdds_cols = ['HDDSStapCer',
             'HDDSStapRoot',
             'HDDSPulse',
             'HDDSDairy',
             'HDDSPrMeatF',
             'HDDSPrMeatO',
             'HDDSPrFish',
             'HDDSPrEggs',
             'HDDSVeg',
             'HDDSFruit',
             'HDDSFat',
             'HDDSSugar',
             'HDDSCond']

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
"""
    Calculates the Household Dietary Diversity Score (HDDS) and related flags based on the provided DataFrame.
    
    The HDDS is calculated as the sum of the binary indicators for the 13 food groups. Flags are created to identify various issues with the HDDS data, such as missing values, erroneous values, identical values, and mismatches between the HDDS and Food Consumption Score (FCS) indicators.
    
    The `custom_flag_logic()` method implements the specific HDDS-related flag checks, including:
    - Identical Values (All 0's): Checks if all HDDS food group indicators are 0.
    - FCS-HDDS Mismatches: Checks for mismatches between the FCS and HDDS indicators, such as when FCS is 0 but HDDS is 1, or when FCS is 7 but HDDS is 0.
    """
        def __init__(self, df, low_erroneous, high_erroneous):
        super().__init__(df, 'HDDS', hdds_cols, hdds_flags)
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous
        self.hdds_cols = hdds_cols  # Make hdds_cols a class attribute

        self.FCS_HDDS_PAIRS = {
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

        self.df['HDDS'] = sum(self.df[col] for col in hdds_cols)

        # Create HDDS categories
        bins = [0, 2, 4, self.df['HDDS'].max() + 1]
        labels = ['0-2 food groups (phase 4 to 5)', '3-4 food groups (phase 3)', '5-12 food groups (phase 1 to 2)']
        self.df['HDDSCat_IPC'] = pd.cut(self.df['HDDS'], bins=bins, labels=labels, include_lowest=True)

    def custom_flag_logic(self):
        """
        HDDS checks: not sequentials

        Flags:
        FCS == 0 -> HDDS == 1
        FCS == 7 -> HDDS == 0 (or HDDS == NaN)
        """
        # Identical Values (All 0's)
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_HDDS_Identical_Values'] = \
        (self.df[self.hdds_cols].sum(axis=1) == 0).astype(int)


        for fcs_col, hdds_cols in self.FCS_HDDS_PAIRS.items():
            if type(hdds_cols) == tuple:
                for hdds_col in hdds_cols:
                    try:
                        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_{fcs_col}_mismatch'] = \
                            ((self.df[fcs_col] == 0) & (self.df[hdds_col] == 1)).astype(int) | \
                            ((self.df[fcs_col] == 7) & (self.df[hdds_col] == 0)).astype(int)
                    except KeyError:
                        print(f"KeyError on {fcs_col} and {hdds_col}")
                        continue
            else:
                self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, f'Flag_{self.indicator_name}_{fcs_col}_mismatch'] = \
                            ((self.df[fcs_col] == 0) & (self.df[hdds_cols] == 1)).astype(int) | \
                            ((self.df[fcs_col] == 7) & (self.df[hdds_cols] == 0)).astype(int)
