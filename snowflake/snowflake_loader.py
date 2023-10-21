# snowflake/snowflake_loader.py

from snowflake.snowflake_connection import get_snowflake_connection

def load_data_to_snowflake(data):
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    # Your Snowflake data loading logic here

    cursor.close()
    connection.close()
