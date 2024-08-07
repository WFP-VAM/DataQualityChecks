import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(filename='data_processing_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MasterSheet:
    def __init__(self, df, base_cols):
        self.df = df
        self.base_cols = base_cols
        self.logger = logging.getLogger(__name__)
        
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
            
            self.generate_flag_narrative_final()
            
            # Overall Flag
            flag_overall_cols = [col for col in self.df.columns if col.startswith('Flag_') and col.endswith('_Overall')]
            flag_overall_cols += ["today"]
            flag_narrative_cols = [col for col in self.df.columns if col.startswith('Flag_') and col.endswith('_Narrative')]
            self.df['Flag_All_Indicators'] = self.df[flag_overall_cols].any(axis=1).astype(int)

            # Filtering the Summary Dataset to include only Household with triggered flags
            hh_summary = self.df[self.df['Flag_All_Indicators'] == 1]

            # Specify the columns in the mastersheet
            mastersheet_cols = self.base_cols + flag_narrative_cols + ['Flag_Narrative_Final']

            hh_summary = hh_summary[mastersheet_cols]

            hh_summary = hh_summary.rename(columns={'today': 'date'})
            
            self.logger.info("Filtered MasterSheet dataframe to include only households with triggered flags")
            return hh_summary
        
        except Exception as e:
            self.logger.error(f"Error generating MasterSheet dataframe: {e}")
            return pd.DataFrame()
            
    def generate_flag_narrative_final(self):
        self.logger.info("Generating Flag_Narrative_Final")
        try:
            flag_columns = [col for col in self.df.columns if col.startswith('Flag_') and col.endswith('_Narrative')]
            
            def generate_flag_narrative(row):
                narrative_parts = []
                i = 1
                for col in flag_columns:
                    value = row[col]
                    if len(str(value)) >= 5:
                        narrative_parts.append(f"{i}. {value}")
                        i += 1
                return ' '.join(narrative_parts)
            
            self.df['Flag_Narrative_Final'] = self.df.apply(generate_flag_narrative, axis=1)
            
            self.logger.info("Flag_Narrative_Final generated successfully")
        except Exception as e:
            self.logger.error(f"Error generating Flag_Narrative_Final: {e}")

    def generate_report(self, writer):
        try:
            hh_summary = self.generate_dataframe()
            hh_summary.to_excel(writer, sheet_name='MasterSheet', index=False)
            self.logger.info("Generated MasterSheet report successfully")
            
        except Exception as e:
            self.logger.error(f"Error generating MasterSheet report: {e}")
