import pandas as pd
import numpy as np
from .helpers.base_indicator import BaseIndicator
from .helpers.standard.rcsi import rcsi_cols, rcsi_weights
import logging

logname = "logs/HFC.log"

logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

class rCSI(BaseIndicator):
    
    flags = {
        'Flag_rCSI_Missing_Values': "Missing value(s) in the reduced coping strategies",
        'Flag_rCSI_Erroneous_Values': "Erroneous value(s) (negative or above 7) in the reduced coping strategies",
        'Flag_rCSI_Abnormal_Identical': "The values of all reduced coping strategies are identical",
        'Flag_rCSI_Poor_FCS_and_Zero_rCSI': "The food consumption is poor with no coping (rCSI=0)",
        'Flag_rCSI_Acceptable_FCS_and_High_rCSI': "The food consumption is acceptable and rCSI is high",
        'Flag_rCSI_MealAdult_with_No_Children': "Adults reduced their meal intake for children with no children in HH"
    }
    
    def __init__(self, 
                 df,
                 high_rcsi,
                 low_erroneous,
                 high_erroneous,
                 high_sugar_oil_consumption):
        
        super().__init__(df,
                         'rCSI',
                         rcsi_cols,
                         rCSI.flags,
                         rcsi_weights)
        
        self.cols = rcsi_cols
        self.weights = rcsi_weights
        self.high_rcsi = high_rcsi
        self.low_erroneous = low_erroneous
        self.high_erroneous = high_erroneous
        self.high_sugar_oil_consumption = high_sugar_oil_consumption

    def custom_flag_logic(self):
        logging.info("Custom flag logic for rCSI...")
        mask = self.df[f'Flag_{self.indicator_name}_Erroneous_Values'] == 0
        
        # Identical Values (Except for 0's)
        self.df.loc[mask, 'Flag_rCSI_Abnormal_Identical'] = \
        ((self.df[self.cols].nunique(axis=1) == 1) & (self.df[self.cols].sum(axis=1) != 0)).astype(int)

        # No Coping With Poor Consumption
        fcs_cat_column = 'FCSCat28' if self.high_sugar_oil_consumption else 'FCSCat21'
        self.df.loc[mask, 'Flag_rCSI_Poor_FCS_and_Zero_rCSI'] = \
        ((self.df[fcs_cat_column] == 'Poor') & (self.df['rCSI'] == 0)).astype(int)
        
        # Acceptable FCS and High rCSI
        self.df.loc[mask, 'Flag_rCSI_Acceptable_FCS_and_High_rCSI'] = \
        ((self.df[fcs_cat_column] == 'Poor') & (self.df['rCSI'] >  self.high_rcsi)).astype(int)
        
        # Adults Reducing Meals For Children But There are No Children
        self.df.loc[mask, 'Flag_rCSI_MealAdult_with_No_Children'] = \
        ((self.df['rCSIMealAdult'] > 0) & (self.df['Sum_children'] == 0)).astype(int)

    def calculate_indicators(self):
        logging.info("Calculating rCSI...")
        self.df['rCSI'] = sum(self.df[col] * weight for col, weight in zip(self.cols, self.weights))
        pass
