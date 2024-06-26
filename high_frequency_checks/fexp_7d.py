import pandas as pd
import numpy as np
from .helpers.base_indicator import BaseIndicator

fexp_7d_purch_cols = ['HHExpFCer_Purch_MN_7D',
                        'HHExpFTub_Purch_MN_7D',
                        'HHExpFPuls_Purch_MN_7D',
                        'HHExpFVeg_Purch_MN_7D',
                        'HHExpFFrt_Purch_MN_7D',
                        'HHExpFAnimMeat_Purch_MN_7D',
                        'HHExpFAnimFish_Purch_MN_7D',
                        'HHExpFFats_Purch_MN_7D',
                        'HHExpFDairy_Purch_MN_7D',
                        'HHExpFEgg_Purch_MN_7D',
                        'HHExpFSgr_Purch_MN_7D',
                        'HHExpFCond_Purch_MN_7D',
                        'HHExpFBev_Purch_MN_7D',
                        'HHExpFOut_Purch_MN_7D']

fexp_7d_giftaid_cols = ['HHExpFCer_GiftAid_MN_7D',
                        'HHExpFTub_GiftAid_MN_7D',
                        'HHExpFPuls_GiftAid_MN_7D',
                        'HHExpFVeg_GiftAid_MN_7D',
                        'HHExpFFrt_GiftAid_MN_7D',
                        'HHExpFAnimMeat_GiftAid_MN_7D',
                        'HHExpFAnimFish_GiftAid_MN_7D',
                        'HHExpFFats_GiftAid_MN_7D',
                        'HHExpFDairy_GiftAid_MN_7D',
                        'HHExpFEgg_GiftAid_MN_7D',
                        'HHExpFSgr_GiftAid_MN_7D',
                        'HHExpFCond_GiftAid_MN_7D',
                        'HHExpFBev_GiftAid_MN_7D',
                        'HHExpFOut_GiftAid_MN_7D']

fexp_7d_own_cols = ['HHExpFCer_Own_MN_7D',
                    'HHExpFTub_Own_MN_7D',
                    'HHExpFPuls_Own_MN_7D',
                    'HHExpFVeg_Own_MN_7D',
                    'HHExpFFrt_Own_MN_7D',
                    'HHExpFAnimMeat_Own_MN_7D',
                    'HHExpFAnimFish_Own_MN_7D',
                    'HHExpFFats_Own_MN_7D',
                    'HHExpFDairy_Own_MN_7D',
                    'HHExpFEgg_Own_MN_7D',
                    'HHExpFSgr_Own_MN_7D',
                    'HHExpFCond_Own_MN_7D',
                    'HHExpFBev_Own_MN_7D',
                    'HHExpFOut_Own_MN_7D']

fexp_7d_cols = fexp_7d_purch_cols + fexp_7d_giftaid_cols + fexp_7d_own_cols

fexp_7d_flags = {
    'Flag_FEXP_7D_Missing_Values': "Missing value(s) in the Food Expenditures 7D Module",
    'Flag_FEXP_7D_Erroneous_Values': "Erroneous value(s) in the Food Expenditures 7D Module",
    'Flag_FEXP_7D_Zero_FEXP': "No Food Purchases/GiftAid/OwnProduction Reported in the last 7 days"
}

class FEXP_7D(BaseIndicator):
    def __init__(self, df, low_erroneous, high_erroneous):
        super().__init__(df, 'FEXP_7D', fexp_7d_cols, fexp_7d_flags)
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous

    def custom_flag_logic(self):
        # Custom flag logic specific to Food Expenditures 7D
        print(f"Custom flag logic for {self.indicator_name}...")
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Missing_Values'] == 0, f'Flag_{self.indicator_name}_Zero_FEXP'] = \
            (self.df['HHExpF_1M'] == 0).astype(int)

    def calculate_indicators(self):
        print(f"Calculating indicators for {self.indicator_name}...")
        
        # Fill NaN values in Food Expenditures with 0
        self.df[fexp_7d_cols] = self.df[fexp_7d_cols].fillna(0)
        
        # Calculating Monthly Food Expenditure        
        self.df['HHExpF_1M'] = sum(self.df[col] for col in fexp_7d_cols) / 7 * 30
