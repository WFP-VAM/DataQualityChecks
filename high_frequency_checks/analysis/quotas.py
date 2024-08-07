import pandas as pd
import logging
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from data_bridges_config import DATA_BRIDGES_CONFIG

# Configure logging
logging.basicConfig(filename='quotas_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class QuotasReport:
    def __init__(self, df, admin_columns=None):
        self.df = df
        self.admin_columns = admin_columns or ["ADMIN1Name", "ADMIN2Name", "ADMIN3Name", "ADMIN4Name", "_uuid"]
        self.logger = logging.getLogger(__name__)
        self.ADMIN_AREAS_LABELS = DATA_BRIDGES_CONFIG['admin_areas_labels_file']
        self.ADMIN_AREAS_QUOTAS =  DATA_BRIDGES_CONFIG['admin_areas_quotas_file']	

    def get_admin_areas_quotas(self):
        try:
            admin_areas = pd.read_pickle(self.ADMIN_AREAS_LABELS)
            quotas_areas = pd.read_pickle(self.ADMIN_AREAS_QUOTAS)
            return admin_areas, quotas_areas
        except FileNotFoundError:
            self.logger.error("Admin areas or quotas file not found.")
            return None, None

    def relabel_admin_areas(self, admin_areas):
        admin_data = self.df[self.admin_columns]
        admin_labels = dict(zip(admin_areas['name'], admin_areas['value_label']))
        for col in ['ID01', 'ID02', 'ID03']:
            admin_data.loc[:, col] = admin_data[col].map(admin_labels)
        return admin_data

    def rename_admin_areas(self, admin_data):
        admin_areas_mapping = {
            'ID01': 'ADMIN1Name',
            'ID02': 'ADMIN2Name',
            'ID03': 'ADMIN3Name',
            'ID04LABEL': 'ADMIN4Name',
        }
        return admin_data.rename(columns=admin_areas_mapping)

    def add_survey_count(self, admin_data):
        melted_df = admin_data.melt(id_vars=['_uuid'], var_name='AdminLevel', value_name='AdminName')
        count_df = melted_df.groupby(['AdminLevel', 'AdminName'])._uuid.nunique().reset_index()
        count_df.columns = ['AdminLevel', 'AdminName', 'SurveyCount']
        return count_df

    def add_quotas(self, df, quotas_areas):
        quota_long = quotas_areas.melt(id_vars=['ADMIN2Name', 'SurveyQuota'],
                                       value_vars=['ADMIN4Name'],
                                       var_name='AdminLevel', value_name='AdminName')
        quota_long['AdminName'] = quota_long['AdminName'].str.upper()
        return df.merge(quota_long[['AdminLevel', 'AdminName', 'SurveyQuota', 'ADMIN2Name']], 
                        on=['AdminLevel', 'AdminName'], 
                        how='outer')

    def filter_admin_areas(self, df):
        completion_by_area = df[df["AdminLevel"].isin(["ADMIN4Name"])]
        return completion_by_area.fillna(0)

    def generate_report(self):
        try:
            admin_areas, quotas_areas = self.get_admin_areas_quotas()
            if admin_areas is None or quotas_areas is None:
                return None

            admin_data = self.relabel_admin_areas(admin_areas)
            admin_data = self.rename_admin_areas(admin_data)
            count_df = self.add_survey_count(admin_data)
            result_df = self.add_quotas(count_df, quotas_areas)
            completion_by_area = self.filter_admin_areas(result_df)

            output_path = f"reports/{DATA_BRIDGES_CONFIG['country_name']}_Survey_Completion_Report.csv"
            completion_by_area.to_csv(output_path)
            self.logger.info(f"Report quota generated and saved to {output_path}")
            return completion_by_area
        except Exception as e:
            self.logger.error(f"Error generating quotas report: {e}")
            return None

if __name__ == "__main__":

    dir = os.path.dirname('__file__')
    data_file = os.path.join(dir, 'data/drc_test_data.csv')

    # Example usage
    df = pd.read_csv(data_file)  # Replace with actual data loading

    admin_columns = ["_uuid", "ID01", "ID02",  "ID03", "ID04LABEL"]
    quotas = QuotasReport(df, admin_columns=admin_columns)
    quotas_report =  quotas.generate_report()
    if quotas_report is not None:
        print("Report generated successfully")
    else:
        print("Failed to generate report")
