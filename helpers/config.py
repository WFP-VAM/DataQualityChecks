# Columns of demographics related to male age groups
male_cols = ['HHSize01M',
             'HHSize24M',
             'HHSize511M', 
             'HHSize1217M', 
             'HHSize1859M',
             'HHSize60AboveM']

# Columns of demographics related to female age groups
female_cols = ['HHSize01F',
             'HHSize24F',
             'HHSize511F', 
             'HHSize1217F', 
             'HHSize1859F',
             'HHSize60AboveF']

# Columns of demographics related to adults
adult_cols = ['HHSize1859M',
              'HHSize60AboveM',
              'HHSize1859F',
              'HHSize60AboveF']

# Flags related to Demographics
demo_flags = {
    'Flag_Demo_High_HHSize': "The Household Size is very high (More than 30)",
    'Flag_Demo_Incosistent_HHSize': "Sum of Males and Females does not match the household size",
    'Flag_Demo_No_Adults': "There are no adults in the household",
    'Flag_Demo_plw': "Number of pregnant and lactating females is higher than females aged 12-59",
}

# Columns of food groups related to FCS
fcs_cols = ['FCSStap',
            'FCSPulse',
            'FCSDairy',
            'FCSPr',
            'FCSVeg',
            'FCSFruit',
            'FCSFat',
            'FCSSugar']

# Weights of food groups related to FCS
fcs_weights = [2, 3, 4, 4, 1, 1, 0.5, 0.5]

# Flags related to FCS
fcs_flags = {
    'Flag_FCS_Missing_Values': "Missing value(s) in the consumption of the 8 main food groups",
    'Flag_FCS_Erroneous_Values': "Erroneous value(s) (negative or above 7) in the consumption of the 8 main food groups",
    'Flag_FCS_Abnormal_Identical': "The consumption of all 8 main food groups is identical",
    'Flag_FCS_Low_Staple': "Low staple consumption (below 4)",
    'Flag_FCS_Low_FCS': "Low FCS (10 or below)",
    'Flag_FCS_High_FCS': "High FCS (90 or above)",
    'Flag_FCS_Poor_FCG_Zero_rCSI': "Poor FCG with no coping (rCSI is zero)",
    'Flag_FCS': "One or more FCS flag(s) triggered"
}