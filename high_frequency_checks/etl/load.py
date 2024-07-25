import pandas as pd
from sqlalchemy import create_engine 
import logging
import yaml
import logging 

CONFIG_PATH = r"databridges_api_database_credentials.yaml"

class ExcelExportError(Exception):
    pass

def database_config(yaml_config_path):
    with open(yaml_config_path, "r") as yamlfile:
        database_config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        SERVER = database_config['SERVER']
        DATABASE = database_config["DB_NAME"]
        USERNAME = database_config["DB_USERNAME"]
        PASSWORD = database_config["DB_PASSWORD"]
        conn_str = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server'
        return conn_str
        
conn_str = database_config(CONFIG_PATH)
engine = create_engine(conn_str)

def load_data(df, table_name):
    try:
        df.to_sql(name=table_name, con=engine, if_exists='replace')
        logging.info(f"Loaded to {table_name}")
    except Exception as e:
        logging.error(f"Error {e} when populating {table_name}")