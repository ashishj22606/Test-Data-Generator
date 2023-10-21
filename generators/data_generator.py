import pandas as pd
from faker import Faker
import random

# Initialize the Faker generator
fake = Faker()

def generate_data(num_records):
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