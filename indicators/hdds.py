import pandas as pd
import numpy as np
from helpers.base_indicator import BaseIndicator

# Columns of food groups related to HDDS
hdds_cols = ['HDDSStapCer', 'HDDSStapRoot', 'HDDSPulse', 'HDDSDairy', 'HDDSPrMeatF', 'HDDSPrMeatO', 'HDDSPrFish', 'HDDSPrEggs', 'HDDSVeg', 'HDDSFruit', 'HDDSFat', 'HDDSSugar', 'HDDSCond']

# Flags related to HDDS
hdds_flags = {
    'Flag_HDDS_Missing_Values': "Missing value(s) in the consumption of the food groups",
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

    def calculate_fcs(self):
        print("Calculating HDDS...")
        pass

    def custom_flag_logic(self):
        column_pairs = {
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

        for key, cols in column_pairs.items():
            fcs_col, *hdds_cols = cols
            fcs_value = self.df[fcs_col]
            hdds_values = [self.df[col] for col in hdds_cols]

        # Check for mismatches
        if fcs_value == 7 and any(value == 0 for value in hdds_values):
            self.df[f"Flag_{self.indicator_name}{key}_mismatch"] = True

        return self.df

        # if self.df["FCSStap"] == 7 and (selfdf["HDDSStapCer"] == 0 or self.df["HDDSStapRoot"] == 0):
        #     df[f"Flag_{self.indicator_name}Stap_mismatch"] = True
        
        # # if household has consumped pulse for 0 days in FCS but has not consummed pulse in the last 24hrs
        # if df["HDDSPulse"] == 0 and df["FCSPulse"] == 7:
        #     df[f"Flag_{self.indicator_name}Pulse_mismatch"] = True

        # # check dairy
        # if df["HDDSDairy"] == 0 and df["FCSDairy"] == 7:
        #     df[f"Flag_{self.indicator_name}Dairy_mismatch"] = True

        # # check animal proteins
        # if (df["HDDSPrMeatF"] == 0 or df["HDDSPrMeatO"] == 0 or df["HDDSPrFish"] == 0 or df["HDDSPrEggs"] == 0) and df["FCSPr"] == 7:
        #     df[f"Flag_{self.indicator_name}Pr_mismatch"] = True

        # # check vegetables
        # if df["HDDSVeg"] == 0 and df["FCSVeg"] == 7:
        #     df["Flag_HDDSVeg"] = True

        # # check fruit
        # if df["HDDSFruit"] == 0 and df["FCSFruit"] == 7:
        #     df["Flag_HDDSFruit"] = True

        # # check fat
        # if df["HDDSFat"] == 0 and df["FCSFat"] == 7:
        #     df["Flag_HDDSFat"] = True

        # # check sugar
        # if df["HDDSSugar"] == 0 and df["FCSSugar"] == 7:
        #     df["Flag_HDDSSugar"] = True

        # # check condiments
        # if df["HHDSCond"] == 0 and df["FCSCond"] == 7:
        #     df["Flag_HDDSSugar"] = True


        return  df


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