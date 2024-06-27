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
fcs_weights = [2,
               3,
               4,
               4,
               1,
               1,
               0.5,
               0.5]

# Flags related to FCS
fcs_flags = {
    'Flag_FCS_Missing_Values': "Missing value(s) in the consumption of the 8 main food groups",
    'Flag_FCS_Erroneous_Values': "Erroneous value(s) (negative or above 7) in the consumption of the 8 main food groups",
    'Flag_FCS_Abnormal_Identical': "The consumption of all 8 main food groups is identical",
    'Flag_FCS_Low_Staple': "Low staple consumption (below 4)",
    'Flag_FCS_Low_FCS': "Low FCS (10 or below)",
    'Flag_FCS_High_FCS': "High FCS (90 or above)",
    'Flag_FCS_Poor_FCG_Zero_rCSI': "Poor FCG with no coping (rCSI is zero)",
    'Flag_FCS_Acceptable_FCG_High_rCSI': "Acceptable FCG with High coping (rCSI above 50)",
    'Flag_FCS': "One or more FCS flag(s) triggered"
}
