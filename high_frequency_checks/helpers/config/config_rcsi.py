# Columns of food groups related to rCSI
rcsi_cols = ['rCSILessQlty',
            'rCSIBorrow',
            'rCSIMealSize',
            'rCSIMealAdult',
            'rCSIMealNb']

# Weights of coping strategies related to rCSI
rcsi_weights = [1, 
                2,
                1,
                3,
                1]

# Flags related to rCSI
rcsi_flags = {
    'Flag_rCSI_Missing_Values': "Missing value(s) in the reduced coping strategies",
    'Flag_rCSI_Erroneous_Values': "Erroneous value(s) (negative or above 7) in the reduced coping strategies",
    'Flag_rCSI_Abnormal_Identical': "The values of all reduced coping strategies is identical",
}