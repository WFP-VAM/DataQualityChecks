import pandas as pd
import numpy as np
from .helpers.base_indicator import BaseIndicator
from .helpers.standard.housing import housing_cols, HHDwellType_options, HHTenureType_options, HHWallType_options, HHRoofType_options, HHFloorType_options


class Housing(BaseIndicator):
    
    flags = {
        'Flag_Housing_Missing_Values': "Missing value(s) in the Housing Module",
        'Flag_Housing_Erroneous_Values': "Erroneous value(s) in the Housing Module",
        'Flag_Housing_Displaced_Owner': "HH is displaced and own a residential property"
    }

    def __init__(self, 
                 df,
                 low_erroneous,
                 high_erroneous):
        
        super().__init__(df, 
                         'Housing',
                         housing_cols,
                         Housing.flags,
                         exclude_erroneous_check=housing_cols)
        
        self.cols = housing_cols
        self.HHDwellType_options = HHDwellType_options
        self.HHTenureType_options = HHTenureType_options
        self.HHWallType_options = HHWallType_options
        self.HHRoofType_options = HHRoofType_options
        self.HHFloorType_options = HHFloorType_options
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous

    def custom_flag_logic(self):
        # Custom flag logic specific to Demographics
        print(f"Custom flag logic for {self.indicator_name}...")
        
        # Custom Erroneous value Logic for Housing Columns
        self.df.loc[self.df[f'Flag_{self.indicator_name}_Missing_Values'] == 0, f'Flag_{self.indicator_name}_Erroneous_Values'] = (
            (~self.df['HHDwellType'].isin(self.HHDwellType_options)) | 
            (~self.df['HHTenureType'].isin(self.HHTenureType_options)) | 
            (~self.df['HHWallType'].isin(self.HHWallType_options)) | 
            (~self.df['HHRoofType'].isin(self.HHRoofType_options)) | 
            (~self.df['HHFloorType'].isin(self.HHFloorType_options))
            ).astype(int)
        
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0
                
        # Displaced HH and Ownder of resident
        self.df.loc[mask, 'Flag_Housing_Displaced_Owner'] = (
            (self.df['HHStatus'].isin([1,2])) & (self.df['HHTenureType'] == 1)
        ).astype(int)
                        
    def calculate_indicators(self):
        print(f"Calculating indicators for {self.indicator_name}...")
        
        pass
