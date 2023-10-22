# snowflake/snowflake_loader.py

from snowflake.snowflake_connection import get_snowflake_connection

def create_streams_snowflake(table_name):
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    # Construct the SQL statement to create a stream for the specified table
    create_stream_sql = f"CREATE OR REPLACE STREAM {table_name}_stream ON TABLE {table_name};"

    try:
        cursor.execute(create_stream_sql)
        connection.commit()
        print(f"Stream for {table_name} created successfully.")
    except Exception as e:
        print(f"Error creating stream for {table_name}: {str(e)}")


    cursor.close()
    connection.close()
