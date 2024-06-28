import os
import pandas as pd
from sqlalchemy import create_engine 
from dotenv import load_dotenv
import logging
import yaml
from datetime import date

# load_dotenv()  # take environment variables from .env.

# SERVER = os.getenv("SERVER")
# DATABASE = os.getenv("DB_NAME")
# USERNAME = os.getenv("DB_USERNAME")
# PASSWORD = os.getenv("DB_PASSWORD")

CONFIG_PATH = r"data_bridges_api_config.yaml"
class ExcelExportError(Exception):
    pass

def db_config(yaml_config_path):
    with open(yaml_config_path, "r") as yamlfile:
        db_config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        SERVER = db_config['SERVER']
        DATABASE = db_config["DB_NAME"]
        USERNAME = db_config["DB_USERNAME"]
        PASSWORD = db_config["DB_PASSWORD"]
        conn_str = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server'
        return conn_str
        
conn_str = db_config(CONFIG_PATH)
engine = create_engine(conn_str)


def load_data(path, sheet_name, table_name):
    df = pd.read_excel(path, sheet_name=sheet_name)
    try:
        df.to_sql(name=table_name, con=engine, if_exists='replace')
        print(f"Loaded to {table_name}")
    except Exception as e:
        print(f"Error {e} when populating {table_name}")

# def load_all_to_db(data: tuple, table_names = None):
#     try: 
#         for df, table_name in zip(data, table_names):
#             print("Loading data to database")
#             load_data(df, table_name)
#     except ExcelExportError as e:
#         print(f"Error loading data: {e}")