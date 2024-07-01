import pandas as pd

base_cols = []
review_cols = []
class MasterSheet:

    def __init__(self, df):
        self.df = df
        self.ensure_review_cols()

    def ensure_review_cols(self):
        """Ensure review columns are present in the dataframe."""
        for col in review_cols:
            if col not in self.df.columns:
                self.df[col] = None

    def merge_with_existing_report(new_mastersheet_df, existing_mastersheet_path):
        """Merge new records with existing master sheet without overwriting reviewed rows."""
        try:
            existing_mastersheet_df = pd.read_excel(existing_mastersheet_path, sheet_name='MasterSheet')
            combined_df = pd.concat([existing_mastersheet_df, new_mastersheet_df])
            # Drop duplicates based on '_uuid' and keep the first occurrence (the existing reviewed records)
            combined_df = combined_df.drop_duplicates(subset=['_uuid'], keep='first')
            return combined_df
        except FileNotFoundError:
            # If the file does not exist, return the new master sheet dataframe
            return new_mastersheet_df

    def generate_dataframe(self):
        # Overall Flag
        flag_overall_cols = [col for col in self.df.columns if col.startswith('Flag_') and col.endswith('_Overall')]
        flag_narrative_cols = [col for col in self.df.columns if col.startswith('Flag_') and col.endswith('_Narrative')]
        self.df['Flag_All_Indicators'] = self.df[flag_overall_cols].any(axis=1).astype(int)

        print(f"Generating MasterSheet")
        hh_summary_cols = base_cols + flag_overall_cols + ['Flag_All_Indicators'] + flag_narrative_cols + review_cols
        hh_summary = self.df[hh_summary_cols]
        
        # Filtering the Summary Dataset to include only Household with triggered flags
        hh_filtered = hh_summary[hh_summary['Flag_All_Indicators'] == 1]
        return hh_filtered

    def generate_report(self, writer):
        hh_filtered = self.generate_dataframe()
        hh_filtered.to_excel(writer, sheet_name='MasterSheet', index=False)
