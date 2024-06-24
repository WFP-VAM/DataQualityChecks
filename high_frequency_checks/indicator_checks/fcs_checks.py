import pandas as pd
import numpy as np


class FCSChecks(IndicatorChecks):
    """
    This class contains the FCS checks and flags for the given dataframe
    """
    def __init__(self, self.df):
        super().__init__(self.df)

    def food_consumption_score(self, threshold="21/35"):
        # Calculate FCS and generate FCS Flags---------------------------------------------------------------#
        fcs_cols = ['FCSStap', 'FCSPulse', 'FCSDairy', 'FCSPr', 'FCSVeg', 'FCSFruit', 'FCSFat', 'FCSSugar']
        self.df['FCS'] = (self.df['FCSStap'] * 2 +
                    self.df['FCSPulse'] * 3 +
                    self.df['FCSDairy'] * 4 +
                    self.df['FCSPr'] * 4 +
                    self.df['FCSVeg'] +
                    self.df['FCSFruit'] +            
                    self.df['FCSFat'] * 0.5 +
                    self.df['FCSSugar'] * 0.5)


        # Create FCG groups based on 21/35 or 28/42 thresholds ------------------------#
        if threshold == "21/35": 
            sugar_thresholds = [0, 21.5, 35.5, float('inf')]
            self.df['FCSCat21'] = pd.cut(self.df['FCS'], bins=sugar_thresholds, labels=['Poor', 'Borderline', 'Acceptable'], right=False)
        elif threshold == "28/42":
            sugar_thresholds = [0, 28.5, 42.5, float('inf')]
            self.df['FCSCat28'] = pd.cut(self.df['FCS'], bins=high_sugar_thresholds, labels=['Poor', 'Borderline', 'Acceptable'], right=False)
        else:
             raise ValueError("Threshold must be either '21/35' or '28/42'")

        return self.self.df
    
    def run_checks(self):
        # Define FCS flags
        fcs_flags = {
            'Flag_FCS_Missing_Values': 
                "One or more values in the FCS Module are missing!",
            'Flag_FCS_Erroneous_Values': 
                "One or more values in the FCS Module have Erroneous values (<0 or >7)",
            'Flag_FCS_Abnormal_Zeroes': 
                "All values in the FCS food groups are filled with 1's",
            'Flag_FCS_Abnormal_Sevens': 
                "All values in the FCS food groups are filled with 7's",
            'Flag_FCS_Abnormal_Identical': 
                "All values in the FCS food groups have the same value",
            'Flag_FCS_Low_Staple': 
                "Low Staple (Below 4)",
            'Flag_FCS_Low_FCS': 
                "Low FCS (10 or Below)",
            'Flag_FCS_High_FCS': 
                "High FCS (90 or Above)"
        }

        # Initialize flags
        for flag in fcs_flags.keys():
            self.df[flag] = np.nan

        # 1. Flag_FCS_Missing_Values: 1 if any column in FCS columns has missing values
        self.df['Flag_FCS_Missing_Values'] = self.df[fcs_cols].isnull().any(axis=1).astype(int)

        # 2. Flag_FCS_Erroneous_Values: 1 if any value in FCS columns is < 0 or > 7, but only if Flag_FCS_Missing_Values is 0
        condition = (self.df[fcs_cols] < 0) | (self.df[fcs_cols] > 7)
        self.df.loc[self.df['Flag_FCS_Missing_Values'] == 0,
            'Flag_FCS_Erroneous_Values'] = condition.any(axis=1).astype(int)

        # 3. Flag_FCS_Abnormal_Zeroes: 1 if all values in FCS columns are 0, but only flag if Flag_FCS_Erroneous_Values is 0
        zero_condition = (self.df[fcs_cols] == 0).all(axis=1)
        self.df.loc[self.df['Flag_FCS_Erroneous_Values'] == 0,
            'Flag_FCS_Abnormal_Zeroes'] = zero_condition.astype(int)

        # 4. Flag_FCS_Abnormal_Sevens: 1 if all values in FCS columns are 7, but only flag if Flag_FCS_Abnormal_Zeroes is 0
        seven_condition = (self.df[fcs_cols] == 7).all(axis=1)
        self.df.loc[self.df['Flag_FCS_Abnormal_Zeroes'] == 0,
            'Flag_FCS_Abnormal_Sevens'] = seven_condition.astype(int)

        # 5. Flag_FCS_Abnormal_Identical: 1 if all values in FCS columns are identical, but only flag if Flag_FCS_Abnormal_Sevens is 0
        identical_condition = self.df[fcs_cols].nunique(axis=1) == 1
        self.df.loc[self.df['Flag_FCS_Abnormal_Sevens'] == 0,
            'Flag_FCS_Abnormal_Identical'] = identical_condition.astype(int)

        # 6. Flag_FCS_Low_Staple: 1 if the value in FCSStap is Below 4, but only flag if Flag_FCS_Abnormal_Sevens is 0
        low_staple_condition = self.df['FCSStap'] < 4
        self.df.loc[self.df['Flag_FCS_Abnormal_Sevens'] == 0, 
            'Flag_FCS_Low_Staple'] = low_staple_condition.astype(int)

        # 7. Flag_FCS_Low_FCS: 1 if the value in FCS is 10 or Below, but only flag if Flag_FCS_Abnormal_Sevens is 0
        low_fcs_condition = self.df['FCS'] <= 10
        self.df.loc[self.df['Flag_FCS_Abnormal_Sevens'] == 0, 
            'Flag_FCS_Low_FCS'] = low_fcs_condition.astype(int)

        # 8. Flag_FCS_High_FCS: 1 if the value in FCS is 90 or Above, but only flag if Flag_FCS_Abnormal_Sevens is 0
        high_fcs_condition = self.df['FCS'] >= 90
        self.df.loc[self.df['Flag_FCS_Abnormal_Sevens'] == 0, 
            'Flag_FCS_High_FCS'] = high_fcs_condition.astype(int)

        # Set Flag_FCS to 1 if any of the columns in fcs_flag_columns have the value 1, else 0
        self.df['Flag_FCS'] = (self.df[list(fcs_flags.keys())] == 1).any(axis=1).astype(int)

        # Build narrative based on flags
        self.df['Flag_FCS_Narrative'] = self.df[fcs_flags.keys()].apply(lambda row: " & ".join([fcs_flags[flag] for flag in fcs_flags if row[flag] == 1]), axis=1)

        # Summarize flags for each household
        hh_summary = self.df[['EnuName', 'FCSStap', 'FCSPulse', 'FCSDairy', 'FCSPr', 'FCSVeg', 'FCSFruit', 'FCSFat', 'FCSSugar', 'Flag_FCS_Missing_Values',
                    'Flag_FCS_Erroneous_Values', 'Flag_FCS_Abnormal_Zeroes', 'Flag_FCS_Abnormal_Sevens', 'Flag_FCS_Abnormal_Identical',
                    'Flag_FCS_Low_Staple', 'Flag_FCS_Low_FCS', 'Flag_FCS_High_FCS', 'Flag_FCS', 'Flag_FCS_Narrative']]

        # Summarize flags for each enumerator with Total_Records and Error_Percentage
        enu_summary = self.df.groupby('EnuName').agg({
            **{key: 'sum' for key in fcs_flags},  # Sum of all flag columns
            'EnuName': 'size',  # Total records per enumerator
            'Flag_FCS': 'sum'  # Sum of Flag_FCS
        }).rename(columns={'EnuName': 'Total_Records'}).reset_index()

        # Calculate Error Percentage
        enu_summary['Error_Percentage'] = (enu_summary['Flag_FCS'] / enu_summary['Total_Records'])

        # Summarize flags for each ID02 and EnuName with Total_Records and Error_Percentage
        id02_enu_summary = self.df.groupby(['ID02', 'EnuName']).agg({
            **{key: 'sum' for key in fcs_flags},  # Sum of all flag columns
            'EnuName': 'size',  # Total records per enumerator
            'Flag_FCS': 'sum'  # Sum of Flag_FCS
        }).rename(columns={'EnuName': 'Total_Records'}).reset_index()

        # Calculate Error Percentage
        id02_enu_summary['Error_Percentage'] = (id02_enu_summary['Flag_FCS'] / id02_enu_summary['Total_Records'])

