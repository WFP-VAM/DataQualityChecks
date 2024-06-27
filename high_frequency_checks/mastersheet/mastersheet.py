import pandas as pd
import numpy as np

class MasterSheet:

    def __init__(self, df):
        self.df = df

    def generate_report(self, writer):
        print("Custom flag logic for MasterSheet...")
        # Overall Flag
        flag_overall_cols = [col for col in self.df.columns if col.startswith('Flag_') and col.endswith('_Overall')]
        flag_narrative_cols = [col for col in self.df.columns if col.startswith('Flag_') and col.endswith('_Narrative')]
        self.df['Flag_All_Indicators'] = self.df[flag_overall_cols].any(axis=1).astype(int)

        print(f"Generating MasterSheet")
        hh_summary_cols = ['_uuid', 'EnuName', 'EnuSupervisorName', 'ID01', 'ID02', 'ID03', 'ID04', 'Flag_All_Indicators'] + flag_overall_cols + flag_narrative_cols
        hh_summary = self.df[hh_summary_cols]
        
        # Filtering the Summary Dataset to include only Household with triggered flags
        hh_filtered = hh_summary[hh_summary[f'Flag_All_Indicators'] == 1]
        hh_filtered.to_excel(writer, sheet_name='MasterSheet', index=False)
