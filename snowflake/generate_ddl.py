from snowflake.snowflake_connection import get_snowflake_connection

def generate_ddl(table_name):
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    # Define the column names and their corresponding data types
    table_columns = {
        "member_id": "INTEGER",
        "contract_no": "INTEGER",
        "dob": "DATE",
        "firstname": "STRING",
        "lastname": "STRING",
        "city": "STRING",
        "state": "STRING",
        "country": "STRING",
        "address": "STRING",
        "phone_no": "STRING"
    }

    ddl = f"CREATE OR REPLACE TABLE {table_name} ("

    for col, dtype in table_columns.items():
        ddl += f" {col} {dtype},"

    ddl = ddl.rstrip(",\n")  # Remove trailing comma and newline
    ddl += ")"
    cursor.execute(ddl)
    cursor.close()
    connection.close()
    return