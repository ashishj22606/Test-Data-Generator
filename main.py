# main.py

from generators.data_generator import generate_name
from snowflake.snowflake_loader import load_data_to_snowflake

def main():
    data = generate_name()  # Generate test data
    load_data_to_snowflake(data)  # Send data to Snowflake

if __name__ == "__main__":
    main()
