import pandas as pd
import numpy as np
from helpers.base_indicator import BaseIndicator

lcs_stress_cols = ['LcsR_stress_Animals',
                    'Lcs_stress_Saving',
                    'Lcs_stress_DomAsset',
                    'Lcs_stress_ConsActive',
                    'Lcs_stress_SellFoodRation',
                    'Lcs_stress_SellNFIRation',
                    'Lcs_stress_EatOut',
                    'Lcs_stress_BorrowCash',
                    'Lcs_stress_Pawn',
                    'Lcs_stress_LessSchool',
                    'Lcs_stress_Utilities',
                    'Lcs_stress_Edu']

lcs_crisis_cols = ['Lcs_crisis_ProdAsset',
                    'Lcs_crisis_Barter',
                    'Lcs_crisis_Health',
                    'Lcs_crisis_Housing',
                    'Lcs_crisis_HHSeparation',
                    'Lcs_crisis_OutSchool',
                    'Lcs_crisis_Migration',
                    'Lcs_crisis_DomMigration',
                    'Lcs_crisis_ChildWork',
                    'LcsR_crisis_AgriCare',
                    'LcsR_crisis_ImmCrops',
                    'LcsR_crisis_Seed']

lcs_em_cols = ['Lcs_em_ChildMigration',
                'Lcs_em_IllegalAct',
                'Lcs_em_Begged',
                'Lcs_em_Marriage',
                'Lcs_em_ResAsset',
                'LcsR_em_FemAnimal',
                'LcsR_em_WildFood']

lcs_children_cols = ['Lcs_stress_LessSchool',
                    'Lcs_crisis_OutSchool',
                    'Lcs_crisis_ChildWork',
                    'Lcs_em_ChildMigration',
                    'Lcs_em_Marriage']

lcs_options = [10, 20, 30, 9999]

# Flags related to rCSI
lcs_flags = {
    'Flag_LCS_Missing_Values': "Missing value(s) in the livelihood coping strategies",
    'Flag_LCS_Erroneous_Values': "Erroneous value(s) in the livelihood coping strategies",
    'Flag_LCS_ChildrenStrategies_with_No_Children': "HH Applied strategies related to children with no children"
}

class LCS(BaseIndicator):
    def __init__(self, df, low_erroneous, high_erroneous):
        self.df = df
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous
        self.lcs_options = lcs_options
        self.lcs_stress_cols = [col for col in lcs_stress_cols if col in self.df.columns]
        self.lcs_crisis_cols = [col for col in lcs_crisis_cols if col in self.df.columns]
        self.lcs_em_cols = [col for col in lcs_em_cols if col in self.df.columns]
        self.lcs_cols = self.lcs_stress_cols + self.lcs_crisis_cols + self.lcs_em_cols
        super().__init__(df, 'LCS', self.lcs_cols, lcs_flags, exclude_erroneous_check=self.lcs_cols)
        
    def custom_flag_logic(self):
        print("Custom flag logic for LCS...")

        # Custom Erroneous value Logic for LCS Columns
        self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] = (
            ~self.df[self.lcs_cols].isin(self.lcs_options).all(axis=1)
        ).astype(int)
        
        # HH Applying livelihood strategies related to children But There are No Children
        children_cols_present = [col for col in lcs_children_cols if col in self.df.columns]
        if children_cols_present:
            self.df[f'Flag_{self.indicator_name}_ChildrenStrategies_with_No_Children'] = (
                (self.df['Sum_children'] == 0) & 
                self.df[children_cols_present].isin([20, 30]).any(axis=1)
            ).astype(int)
        else:
            self.df[f'Flag_{self.indicator_name}_ChildrenStrategies_with_No_Children'] = 0
            

    def calculate_indicators(self):
        pass
    