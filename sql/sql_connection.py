import pyodbc
from config.config_data import PersonData as pers_data
from config import env_config as env
username = pers_data.sql_login
password = pers_data.sql_password


class SQLConnection:

    def __init__(self):
        self.connection = pyodbc.connect(
            f"DRIVER={{SQL Server}}; SERVER={env.config['dataBase_QA']}; DATABASE={env.config['table_QA']}", autocommit=True)
        self.connection_ESD = pyodbc.connect(
            f"DRIVER={{SQL Server}}; SERVER={env.config['dataBase_ESD']}; DATABASE={env.config['table_ESD']}", autocommit=True)
        self.cursor = self.connection.cursor()
        self.cursor_ESD = self.connection_ESD.cursor()



