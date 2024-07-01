import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(filename='data_processing_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MasterSheet:
    def __init__(self, df, base_cols, review_cols):
        self.df = df
        self.base_cols = base_cols
        self.review_cols = review_cols
        self.ensure_review_cols()
        self.logger = logging.getLogger(__name__)

    def ensure_review_cols(self):
        """Ensure review columns are present in the dataframe."""
        for col in self.review_cols:
            if col not in self.df.columns:
                self.df[col] = None
        
    @staticmethod
    def merge_with_existing_report(new_mastersheet_df, existing_mastersheet_path):
        """Merge new records with existing master sheet without overwriting reviewed rows."""
        try:
            if os.path.exists(existing_mastersheet_path):
                existing_mastersheet_df = pd.read_excel(existing_mastersheet_path, sheet_name='MasterSheet')
                combined_df = pd.concat([existing_mastersheet_df, new_mastersheet_df])
                # Drop duplicates based on '_uuid' and keep the first occurrence (the existing reviewed records)
                combined_df = combined_df.drop_duplicates(subset=['_uuid'], keep='first')
                logging.info(f"Successfully merged new master sheet with existing master sheet: {existing_mastersheet_path}")
            else:
                logging.info(f"Existing master sheet not found at path: {existing_mastersheet_path}. Using new master sheet only.")
                combined_df = new_mastersheet_df
            return combined_df
        
        except Exception as e:
            logging.error(f"Error merging with existing master sheet: {e}")
            return new_mastersheet_df

    def generate_dataframe(self):
        try:
            # Overall Flag
            flag_overall_cols = [col for col in self.df.columns if col.startswith('Flag_') and col.endswith('_Overall')]
            flag_narrative_cols = [col for col in self.df.columns if col.startswith('Flag_') and col.endswith('_Narrative')]
            self.df['Flag_All_Indicators'] = self.df[flag_overall_cols].any(axis=1).astype(int)

            # Filtering the Summary Dataset to include only Household with triggered flags
            hh_summary = self.df[self.df['Flag_All_Indicators'] == 1]

            # Specify the columns in the mastersheet
            mastersheet_cols = self.base_cols + flag_narrative_cols + self.review_cols

            hh_summary = hh_summary[mastersheet_cols]

            self.logger.info("Filtered MasterSheet dataframe to include only households with triggered flags")
            return hh_summary
        
        except Exception as e:
            self.logger.error(f"Error generating MasterSheet dataframe: {e}")
            return pd.DataFrame()


    def generate_report(self, writer):
        try:
            hh_summary = self.generate_dataframe()
            hh_summary.to_excel(writer, sheet_name='MasterSheet', index=False)
            self.logger.info("Generated MasterSheet report successfully")
            
        except Exception as e:
            self.logger.error(f"Error generating MasterSheet report: {e}")
