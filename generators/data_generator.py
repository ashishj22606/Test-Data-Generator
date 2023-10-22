import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import random

# Initialize the Faker generator
fake = Faker()

def generate_data_member(num_records):
    data = {
        "member_id": [fake.unique.random_int(min=1, max=10000) for _ in range(num_records)],
        "contract_no": [fake.unique.random_int(min=10000, max=99999) for _ in range(num_records)],
        "dob": [fake.date_of_birth(minimum_age=18, maximum_age=65).strftime('%Y-%m-%d') for _ in range(num_records)],
        "firstname": [fake.first_name() for _ in range(num_records)],
        "lastname": [fake.last_name() for _ in range(num_records)],
        "city": [fake.city() for _ in range(num_records)],
        "state": [fake.state() for _ in range(num_records)],
        "country": ["US" for _ in range(num_records)],
        "address": [fake.street_address() for _ in range(num_records)],
        "phone_no": ['{}-{}-{}'.format(''.join(random.choices('0123456789', k=3)),
                                     ''.join(random.choices('0123456789', k=3)),
                                     ''.join(random.choices('0123456789', k=4))) for _ in range(num_records)]
    }

    df = pd.DataFrame(data)
    return df

def generate_membership_plan_data(existing_df):
    # Extract the existing member IDs
    member_ids = existing_df["member_id"]

    # Generate random membership plan, plan code, and effective date
    membership_data = {
        "member_id": member_ids,
        "plan": [random.choice(["HA", "BA", "FEP", "ITS"]) for _ in range(len(member_ids))],
        "plan_code": [random.choice([23, 65, 34, 43]) for _ in range(len(member_ids))],
        "eff_date": [fake.date_between_dates(date_start=datetime(2023, 1, 1), date_end=datetime(2023, 12, 31)).strftime('%Y-%m-%d') for _ in range(len(member_ids))]
    }

    # Create a DataFrame for membership data
    membership_df = pd.DataFrame(membership_data)

    return membership_df