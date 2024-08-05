
from data_bridges_knots import DataBridgesShapes, get_value_labels
from data_bridges_config import DATA_BRIDGES_CONFIG
import pandas as pd

ADMIN_AREAS_LABELS = "data/drc_admin_labels.csv"
ADMIN_AREAS_QUOTAS = "data/drc_sampling_size.xlsx"

def get_admin_areas_quotas(admin_areas, admin_quotas): 
    # Extract admin areas labels
    admin_areas = pd.read_csv(admin_areas)
    # Extract quotas
    quotas_areas = pd.read_excel(admin_quotas)
    return admin_areas, quotas_areas

def relabel_admin_areas(df, admin_columns, admin_areas):
    admin_data = df[admin_columns]
    admin_labels = dict(zip(admin_areas['name'], admin_areas['value_label']))

    admin_data['ID01'] = admin_data['ID01'].map(admin_labels)
    admin_data['ID02'] = admin_data['ID02'].map(admin_labels)
    admin_data['ID03'] = admin_data['ID03'].map(admin_labels)
    return admin_data

def rename_admin_areas(admin_data):
    admin_areas_mapping = {
    'ID01': 'ADMIN1Name',
    'ID02': 'ADMIN2Name',
    'ID03': 'ADMIN3Name',
    'ID04LABEL': 'ADMIN4Name',
}

    admin_data = admin_data.rename(columns=admin_areas_mapping)
    return admin_data

def add_survey_count(admin_data):
    melted_df = admin_data.melt(id_vars=['_uuid'], var_name='AdminLevel', value_name='AdminName')

    count_df = melted_df.groupby(['AdminLevel', 'AdminName'])._uuid.nunique().reset_index()
    count_df.columns = ['AdminLevel', 'AdminName', 'SurveyCount']
    return count_df

def add_quotas(df, quotas_areas):
    quota_long = quotas_areas.melt(id_vars= ['ADMIN2Name','SurveyQuota'],
                             value_vars=['ADMIN4Name'],
                             var_name='AdminLevel', value_name='AdminName')
    quota_long['AdminName'] = quota_long['AdminName'].str.upper()

    result_df = df.merge(quota_long[['AdminLevel', 'AdminName', 'SurveyQuota', 'ADMIN2Name']], 
                           on=['AdminLevel', 'AdminName'], 
                           how='outer')
                               
    return result_df

def filter_admin_areas(df):
    completion_by_area = df[df["AdminLevel"].isin(["ADMIN4Name"])]
    completion_by_area = completion_by_area.fillna(0)
    return completion_by_area

def generate_quotas_report(df, admin_columns = None):
    if admin_columns == None:
        admin_columns = ["ADMIN1Name", "ADMIN2Name", "ADMIN3Name", "ADMIN4Name", "_uuid"]

    try:
        admin_areas, admin_quotas = get_admin_areas_quotas(ADMIN_AREAS_LABELS, ADMIN_AREAS_QUOTAS)

        admin_data = relabel_admin_areas(df, admin_columns, admin_areas)

        admin_data = rename_admin_areas(admin_data)

        count_df = add_survey_count(admin_data)

        result_df = add_quotas(count_df, admin_quotas)

        completion_by_area = filter_admin_areas(result_df)
        completion_by_area.to_csv(f"reports/{DATA_BRIDGES_CONFIG["country_name"]}_Survey_Completion_Report.csv")
        print("Report quota generated")
    except FileNotFoundError:
        print("Data files not found. Survey completion report not generated.")


if __name__ == "__main__":
    pass


