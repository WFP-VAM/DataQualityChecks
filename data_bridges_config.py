DATA_BRIDGES_CONFIG = {
    # "questionnaire_id": 1737,# OLD
    # "survey_id": 3607,   # OLD
    "questionnaire_id": 1740,
    "survey_id": 3653, 
    "country_name": "DRC",
    "credentials_file_path": r"databridges_api_database_credentials.yaml",
    "data_file_extract": r"data/drc_efsa_data.csv", # BACKUP IF PIPELINE FAILS
    'test_data_file_extract': r"data/drc_test_data.pkl",
    'admin_areas_quotas_file': r"data/drc_sampling_size.pkl",
    'admin_areas_labels_file': r"data/drc_admin_labels.pkl",
}
