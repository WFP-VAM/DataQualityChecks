"""
Run the data quality checks
"""
import pandas as pd
from data_bridges_knots import DataBridgesShapes
from indicator_checks import IndicatorChecks, FCSChecks

CONFIG_PATH = r"data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

#%% XSLForm definition and Household dataset

CONGO_CFSVA = {
    'questionnaire': 1509,
    'dataset': 3094
}
# get household survey data  
data = client.get_household_survey(survey_id=CONGO_CFSVA["dataset"], access_type='full')
# get XLSForm data
questionnaire = client.get_household_questionnaire(CONGO_CFSVA["questionnaire"])

# Run FCS checks
fcs_checks = FCSChecks(data)
fcs_checks.run_checks()




# # Write to Excel with two sheets: HH_Report and Enu_Report
# with pd.ExcelWriter('output/HFC_Report.xlsx') as writer:
#     hh_summary.to_excel(writer, sheet_name='HH_Report', index=False)
#     enu_summary.to_excel(writer, sheet_name='Enu_Report', index=False)
#     id02_enu_summary.to_excel(writer, sheet_name='Admin2_Enu_Report', index=False)
