import pandas as pd
import numpy as np
from helpers.base_indicator import BaseIndicator

nfexp_1m_purch_cols = ['HHExpNFHyg_Purch_MN_1M',
                        'HHExpNFTransp_Purch_MN_1M',
                        'HHExpNFFuel_Purch_MN_1M',
                        'HHExpNFWat_Purch_MN_1M',
                        'HHExpNFElec_Purch_MN_1M',
                        'HHExpNFEnerg_Purch_MN_1M',
                        'HHExpNFDwelSer_Purch_MN_1M',
                        'HHExpNFPhone_Purch_MN_1M',
                        'HHExpNFRecr_Purch_MN_1M',
                        'HHExpNFAlcTobac_Purch_MN_1M']

nfexp_1m_giftaid_cols = ['HHExpNFHyg_GiftAid_MN_1M',
                            'HHExpNFTransp_GiftAid_MN_1M',
                            'HHExpNFFuel_GiftAid_MN_1M',
                            'HHExpNFWat_GiftAid_MN_1M',
                            'HHExpNFElec_GiftAid_MN_1M',
                            'HHExpNFEnerg_GiftAid_MN_1M',
                            'HHExpNFDwelSer_GiftAid_MN_1M',
                            'HHExpNFPhone_GiftAid_MN_1M',
                            'HHExpNFRecr_GiftAid_MN_1M',
                            'HHExpNFAlcTobac_GiftAid_MN_1M']

nfexp_1m_cols = nfexp_1m_purch_cols + nfexp_1m_giftaid_cols

nfexp_1m_flags = {
    'Flag_NFEXP_1M_Missing_Values': "Missing value(s) in the Non-Food Expenditures 1M Module",
    'Flag_NFEXP_1M_Erroneous_Values': "Erroneous value(s) in the Non-Food Expenditures 1M Module",
}

class NFEXP_1M(BaseIndicator):
    def __init__(self, df, low_erroneous, high_erroneous):
        super().__init__(df, 'NFEXP_1M', nfexp_1m_cols, nfexp_1m_flags, exclude_missing_check=nfexp_1m_cols)
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous

    def custom_flag_logic(self):
        # Custom flag logic specific to Non-Food Expenditures 1M
        print(f"Custom flag logic for {self.indicator_name}...")
        
        # Custom Missing Values Logic for NFEXP_1M
        for col in nfexp_1m_cols:
            base_col = col.replace('_MN', '')
            self.df[f'Flag_{self.indicator_name}_Missing_Values'] = (
                (self.df[base_col] == 1) & self.df[col].isnull()
            ).astype(int)

    def calculate_indicators(self):
        print(f"Calculating indicators for {self.indicator_name}...")
        
        # Calculating Monthly Non-Food Expenditure 1M
        self.df['HHExpNF_1M_1M'] = sum(self.df[col] for col in nfexp_1m_cols)
