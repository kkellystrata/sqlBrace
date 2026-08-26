"""Connect to SQL Server and list table names."""

import os

import pyodbc
from dotenv import load_dotenv


def get_table_names(server, database, username=None, password=None, driver="ODBC Driver 18 for SQL Server"):
    if username and password:
        conn_str = (
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
            f"UID={username};PWD={password}"
        )
    else:
        conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        return [row.TABLE_NAME for row in cursor.fetchall()]


if __name__ == "__main__":
    load_dotenv()

    tables = get_table_names(
        server=os.environ["SQLBRACE_SERVER"],
        database=os.environ["SQLBRACE_DATABASE"],
        username=os.environ.get("SQLBRACE_USERNAME"),
        password=os.environ.get("SQLBRACE_PASSWORD"),
    )
    for name in tables:
        print(name)
