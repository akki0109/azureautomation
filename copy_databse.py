import pyodbc
import os

# Azure SQL Database connection strings
src_db_conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=<source_database_server>;DATABASE=<source_database_name>;UID=<source_database_username>;PWD=<source_database_password>"
dst_db_conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=<destination_database_server>;DATABASE=<destination_database_name>;UID=<destination_database_username>;PWD=<destination_database_password>"

def copy_database():
    # Connect to source database
    src_conn = pyodbc.connect(src_db_conn_str)
    src_cursor = src_conn.cursor()

    # Connect to destination database
    dst_conn = pyodbc.connect(dst_db_conn_str)
    dst_cursor = dst_conn.cursor()

    # Get schema from source database
    src_schema = src_cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'").fetchall()

    # Create tables in destination database
    for table in src_schema: 
        table_name = table[0]
        create_table_sql = src_cursor.execute(f"SELECT OBJECT_DEFINITION(OBJECT_ID('{table_name}'))").fetchone()[0]
        dst_cursor.execute(create_table_sql)

    # Copy data from source database to destination database
    for table in src_schema:
        table_name = table[0]
        copy_data_sql = f"INSERT INTO {table_name} SELECT * FROM {table_name}"
        dst_cursor.execute(copy_data_sql)

    # Commit changes
    dst_conn.commit()

    # Close connections
    src_conn.close()
    dst_conn.close()
