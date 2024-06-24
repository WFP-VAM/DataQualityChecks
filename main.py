"""
Run the data quality checks
"""
import pandas as pd
from data_bridges_knots import DataBridgesShapes
from high_frequency_checks import run_fcs_checks

data = pd.read_csv("static/congo.csv")

# Run FCS checks
run_fcs_checks(data, report="static/FCS_report.xlsx")