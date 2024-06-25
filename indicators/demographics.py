import pandas as pd
import numpy as np
from helpers.base_indicator import BaseIndicator

male_cols = ['HHSize01M',
             'HHSize24M',
             'HHSize511M',
             'HHSize1217M',
             'HHSize1859M',
             'HHSize60AboveM']

female_cols = ['HHSize01F',
               'HHSize24F',
               'HHSize511F',
               'HHSize1217F',
               'HHSize1859F',
               'HHSize60AboveF']

adult_cols = ['HHSize1859M',
              'HHSize60AboveM',
              'HHSize1859F',
              'HHSize60AboveF']

demo_flags = {
    'Flag_Demo_Missing_Values': "Missing value(s) in the Demographics Module",
    'Flag_Demo_Erroneous_Values': "Erroneous value(s) in the Demographics Module",
    'Flag_Demo_High_HHSize': "The Household Size is very high (More than 30)",
    'Flag_Demo_Inconsistent_HHSize': "Sum of Males and Females does not match the household size",
    'Flag_Demo_No_Adults': "There are no adults in the household",
    'Flag_Demo_plw': "Number of pregnant and lactating females is higher than females aged 12-59"
}

class Demo(BaseIndicator):
    def __init__(self, df, high_hhsize, low_erroneous, high_erroneous):
        super().__init__(df, 'Demo', ['HHSize', 'HHPregLactNb'] + male_cols + female_cols , demo_flags)
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous
        self.high_hhsize = high_hhsize

    def custom_flag_logic(self):
        # Custom flag logic specific to Demographics
        print(f"Custom flag logic for {self.indicator_name}...")

        # High Household Size
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_Demo_High_HHSize'] = \
            (self.df['HHSize'] > self.high_hhsize).astype(int)

        # Inconsistent Household Size
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_Demo_Inconsistent_HHSize'] = \
            ((self.df['Sum_M'] + self.df['Sum_F']) != self.df['HHSize']).astype(int)

        # No Adults
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_Demo_No_Adults'] = \
            (self.df[adult_cols].sum(axis=1) == 0).astype(int)
        
        # Pregnant and Lactating Women vs Adult Females
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0, 'Flag_Demo_plw'] = \
            (self.df['HHPregLactNb'] > self.df['in_plw_range']).astype(int)

    def calculate_indicators(self):
        print(f"Calculating indicators for {self.indicator_name}...")
        
        # Fill NaN values in HHPregLactNb with 0
        self.df['HHPregLactNb'].fillna(0, inplace=True)
        
        self.calculate_hh_size()
        self.calculate_total_adults()
        self.calculate_total_plw_range()

    def calculate_hh_size(self):
        print("Calculating household size...")
        self.df['Sum_M'] = self.df[male_cols].sum(axis=1)
        self.df['Sum_F'] = self.df[female_cols].sum(axis=1)
        self.df['Sum_M_F'] = self.df['Sum_M'] + self.df['Sum_F']

    def calculate_total_adults(self):
        print("Calculating total adults...")
        self.df['Sum_adults'] = self.df[adult_cols].sum(axis=1)

    def calculate_total_plw_range(self):
        print("Calculating PLW range...")
        self.df['in_plw_range'] = self.df['HHSize1217F'] + self.df['HHSize1859F']
