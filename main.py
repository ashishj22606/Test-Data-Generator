# main.py

from generators.data_generator import generate_data
from snowflake.snowflake_loader import load_data_to_snowflake
from snowflake.generate_ddl import generate_ddl

def main():
    num_records = 1000
    data_frame = generate_data(num_records) # Generate test data
    print(data_frame)
    table_name_to_create="member_test_kafka_table"
    generate_ddl(table_name_to_create)
    load_data_to_snowflake(data_frame)  # Send data to Snowflake

if __name__ == "__main__":
    main()
