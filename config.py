config = {

    "DataBridgesIDs": {
        'questionnaire': 1509,
        'dataset': 3094
    },
    "CountryName": "DRC",
    
    'FCS': {
        'low_fcs': 10, # If FCS below low_fcs, trigger LOW_FCS
        'high_fcs': 100, # IF FCS above high_fcs, trigger High_FCS
        'low_erroneous': 0, # IF any value in the 8 food groups is below low_erroneous, trigger Erroneous_Values
        'high_erroneous': 7, # IF any value in the 8 food groups is above high_erroneous, trigger Erroneous_Values
        'high_sugar_oil_consumption': True # if True, use Cat28, if false use Cat21
    },
    
    'rCSI': {
        'high_rcsi': 50, # IF FCS above high_rcsi, trigger High_rCSI
        'low_erroneous': 0, # IF any value in the 5 coping strategies is below low_erroneous, trigger Erroneous_Values
        'high_erroneous': 7, # IF any value in the 5 coping strategies is above high_erroneous, trigger Erroneous_Values
        'high_sugar_oil_consumption': True # if True, use Cat28, if false use Cat21
    },
    
    'Demo': {
        'low_erroneous': 0, # IF any value in the age groups is below low_erroneous, trigger Erroneous_Values
        'high_erroneous': 30, # IF any value in the age groups is above high_erroneous, trigger Erroneous_Values
        'high_hhsize': 40 # If household size above high_hhsize, trigger Flag
    },
    
    'HDDS': {
        'low_erroneous': 0,
        'high_erroneous': 1
    },
    
    'FEXP_7D': {
        'low_erroneous': 0, # IF any value in the food expenditures 7D is below low_erroneous, trigger Erroneous_Values
        'high_erroneous': 100000 # IF any value in the food expenditures 7D is above high_erroneous, trigger Erroneous_Values
    },
    
    'NFEXP_1M': {
        'low_erroneous': 0, # IF any value in the non-food expenditures 1M is below low_erroneous, trigger Erroneous_Values
        'high_erroneous': 500000 # IF any value in the non-food expenditures 1M is above high_erroneous, trigger Erroneous_Values
    },
    
    'NFEXP_6M': {
        'low_erroneous': 0, # IF any value in the non-food expenditures 6M is below low_erroneous, trigger Erroneous_Values
        'high_erroneous': 1000000 # IF any value in the non-food expenditures 6M is above high_erroneous, trigger Erroneous_Values
    }, 
    "SURVEYS": {
        "total_surveys": 1000,
        "surveys_admin2": {}
    },
    
    'LCS': {
        'low_erroneous': None,
        'high_erroneous': None
    }

}
