# main.py

from generators.data_generator import generate_data_member
from generators.data_generator import generate_membership_plan_data
from snowflake.snowflake_loader import load_data_to_snowflake
from snowflake.generate_ddl import generate_ddl_member
from snowflake.generate_ddl import generate_ddl_membership_plan
from snowflake.streams_creation import create_streams_snowflake

def main():
    num_records = 1000
    data_frame = generate_data_member(num_records) # Generate test data
    print(data_frame)
    mem_plan_df = generate_membership_plan_data(data_frame)
    print(mem_plan_df)
    table_name_to_create1="member_test_kafka_table"
    table_name_to_create2="member_plan_test_kafka_table"
    generate_ddl_member(table_name_to_create1)
    generate_ddl_membership_plan()
    load_data_to_snowflake(data_frame)  # Send data to Snowflake
    load_data_to_snowflake(mem_plan_df)  # Send data to Snowflake
    create_streams_snowflake()


if __name__ == "__main__":
    main()
