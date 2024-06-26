import pandas as pd
import numpy as np
from helpers.base_indicator import BaseIndicator

nfexp_6m_purch_cols = ['HHExpNFMedServ_Purch_MN_6M',
                        'HHExpNFMedGood_Purch_MN_6M',
                        'HHExpNFCloth_Purch_MN_6M',
                        'HHExpNFEduFee_Purch_MN_6M',
                        'HHExpNFEduGood_Purch_MN_6M',
                        'HHExpNFRent_Purch_MN_6M',
                        'HHExpNFHHSoft_Purch_MN_6M',
                        'HHExpNFHHMaint_Purch_MN_6M']

nfexp_6m_giftaid_cols = ['HHExpNFMedServ_GiftAid_MN_6M',
                        'HHExpNFMedGood_GiftAid_MN_6M',
                        'HHExpNFCloth_GiftAid_MN_6M',
                        'HHExpNFEduFee_GiftAid_MN_6M',
                        'HHExpNFEduGood_GiftAid_MN_6M',
                        'HHExpNFRent_GiftAid_MN_6M',
                        'HHExpNFHHSoft_GiftAid_MN_6M',
                        'HHExpNFHHMaint_GiftAid_MN_6M']

nfexp_6m_cols = nfexp_6m_purch_cols + nfexp_6m_giftaid_cols

nfexp_6m_flags = {
    'Flag_NFEXP_6M_Missing_Values': "Missing value(s) in the Non-Food Expenditures 6M Module",
    'Flag_NFEXP_6M_Erroneous_Values': "Erroneous value(s) in the Non-Food Expenditures 6M Module",
}

class NFEXP_6M(BaseIndicator):
    def __init__(self, df, low_erroneous, high_erroneous):
        super().__init__(df, 'NFEXP_6M', nfexp_6m_cols, nfexp_6m_flags)
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous

    def custom_flag_logic(self):
        # Custom flag logic specific to Non-Food Expenditures 6M
        print(f"Custom flag logic for {self.indicator_name}...")

    def calculate_indicators(self):
        print(f"Calculating indicators for {self.indicator_name}...")
        
        # Fill NaN values in Non-Food Expenditures 6M with 0
        self.df[nfexp_6m_cols] = self.df[nfexp_6m_cols].fillna(0)
        
        # Calculating Monthly Non-Food Expenditures 6M        
        self.df['HHNExpF_6M_1M'] = sum(self.df[col] for col in nfexp_6m_cols)
