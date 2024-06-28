import pandas as pd
import numpy as np
from .helpers.base_indicator import BaseIndicator
from .helpers.standard.demo import male_cols, female_cols, adult_cols, children_cols


class Demo(BaseIndicator):
    
    flags = {
        'Flag_Demo_Missing_Values': "Missing value(s) in the Demographics Module",
        'Flag_Demo_Erroneous_Values': "Erroneous value(s) in the Demographics Module",
        'Flag_Demo_Missing_Plw': "Missing value(s) in PLW",
        'Flag_Demo_Plw_Higher_F1259': "Number of PLW exceeds females 12-59",
        'Flag_Demo_High_HHSize': "The Household Size is very high",
        'Flag_Demo_Inconsistent_HHSize': "Sum of Males and Females does not match the household size",
        'Flag_Demo_No_Adults': "There are no adults in the household",
    }

    def __init__(self, 
                 df,
                 high_hhsize,
                 low_erroneous,
                 high_erroneous):
        
        super().__init__(df, 
                         'Demo',
                         ['HHSize', 'HHPregLactNb'] + male_cols + female_cols , Demo.flags,
                         exclude_missing_check=['HHPregLactNb'])
        
        self.male_cols = male_cols
        self.female_cols = female_cols
        self.adult_cols = adult_cols
        self.children_cols = children_cols
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous
        self.high_hhsize = high_hhsize

    def custom_flag_logic(self):
        # Custom flag logic specific to Demographics
        print(f"Custom flag logic for {self.indicator_name}...")
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0

        # Custom Missing value Logic for HHPregLactNb if there are females between 12 and 59
        self.df.loc[mask, 'Flag_Demo_Missing_Plw'] = ((self.df['in_plw_range'] > 0) & (self.df['HHPregLactNb'].isnull())).astype(int) 
                
        # Pregnant and Lactating Women vs Adult Females
        self.df.loc[mask, 'Flag_Demo_Plw_Higher_F1259'] = (self.df['HHPregLactNb'] > self.df['in_plw_range']).astype(int)
            
        # High Household Size
        self.df.loc[mask, 'Flag_Demo_High_HHSize'] = (self.df['HHSize'] > self.high_hhsize).astype(int)

        # Inconsistent Household Size
        self.df.loc[mask, 'Flag_Demo_Inconsistent_HHSize'] = ((self.df['Sum_M'] + self.df['Sum_F']) != self.df['HHSize']).astype(int)

        # No Adults
        self.df.loc[mask, 'Flag_Demo_No_Adults'] = (self.df[self.adult_cols].sum(axis=1) == 0).astype(int)
            
    def calculate_indicators(self):
        print(f"Calculating indicators for {self.indicator_name}...")
        
        self.calculate_hh_size()
        self.calculate_total_adults()
        self.calculate_total_children()
        self.calculate_total_plw_range()

    def calculate_hh_size(self):
        print("Calculating household size...")
        self.df['Sum_M'] = self.df[self.male_cols].sum(axis=1)
        self.df['Sum_F'] = self.df[self.female_cols].sum(axis=1)
        self.df['Sum_M_F'] = self.df['Sum_M'] + self.df['Sum_F']

    def calculate_total_adults(self):
        print("Calculating total adults...")
        self.df['Sum_adults'] = self.df[self.adult_cols].sum(axis=1)

    def calculate_total_children(self):
        print("Calculating total children...")
        self.df['Sum_children'] = self.df[self.children_cols].sum(axis=1)
        
    def calculate_total_plw_range(self):
        print("Calculating total women/girls between 12 and 59...")
        self.df['in_plw_range'] = self.df['HHSize1217F'] + self.df['HHSize1859F']
