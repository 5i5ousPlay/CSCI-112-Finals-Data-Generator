import uuid
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()


def random_date(start, end):
    """Generate a random date between `start` and `end`."""
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


def generate_uuids(num_ids):
    uuid_list = [str(uuid.uuid4()) for i in range(num_ids)]
    return uuid_list


def generate_user_profile(uuids: list) -> list:
    profiles = []
    for i in range(len(uuids)):
        profile = {
            "id": uuids[i],
            "full_name": fake.name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "middle_name": fake.first_name(),
            "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=65).strftime('%Y-%m-%d'),
            "valid_id_type": random.choice(["Passport", "Driver's License", "National ID"]),
            "valid_id_number": fake.ssn(),
            "self_picture": fake.image_url(),
            "current_add": fake.address(),
            "permanent_add": fake.address(),
            "employment_status": random.choice(["Employed", "Self-Employed", "Unemployed"]),
            "company_working": fake.company(),
            "job_title": fake.job(),
            "income_source": random.choice(["Salary", "Business", "Investment", "Other"]),
            "payslip": fake.file_path(extension="pdf"),
            "updated": datetime.now().isoformat()
        }
        profiles.append(profile)
    return profiles


def generate_application(uuids: dict) -> list:
    applications = []
    for i in range(len(uuids['applications'])):
        application = {
            "id": uuids['applications'][i],
            "user_profile": uuids['users'][i],
            "date_submitted": random_date(datetime.now() - timedelta(days=730), datetime.now()).isoformat(),
            "app_status": random.choice(["Pending", "Approved", "Rejected"]),
            "mode": random.choice(["Online", "In-Person"]),
            "notes": fake.text(max_nb_chars=100),
            "apply_attempt": random.choice([1, 2, 3]),
            "updated": datetime.now().isoformat()
        }
        applications.append(application)

    return applications


def generate_contact_info(num_entries: int, user_ids: list) -> list:
    contacts = []
    for i in range(num_entries):
        contact = {
            "id": str(uuid.uuid4()),
            "user_profile": user_ids[i],
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "tel_number": fake.phone_number(),
            "updated": datetime.now().isoformat()
        }
        contacts.append(contact)
    return contacts


def generate_banking_info(num_entries: int, application_ids: list) -> list:
    bank_info = []
    for i in range(num_entries):
        info = {
            "id": str(uuid.uuid4()),
            "application_id": application_ids[i],
            "bank_name": fake.company(),
            "account_type": random.choice(["Savings", "Checking"]),
            "account_number": random.randint(10000000, 99999999),
            "bank_status": random.choice(["Active", "Inactive"])
        }
        bank_info.append(info)
    return bank_info


def generate_financial_info(num_entries: int, application_ids: list) -> list:
    finances = []
    for i in range(num_entries):
        finance = {
            "id": str(uuid.uuid4()),
            "application_id": application_ids[i],
            "income": round(random.uniform(20000, 200000), 2),
            "net_assets": round(random.uniform(50000, 500000), 2),
            "net_debt": round(random.uniform(0, 200000), 2),
            "updated": datetime.now().isoformat()
        }
        finances.append(finance)
    return finances


def generate_credit_account(uuids: list) -> list:
    accounts = []
    for i in range(len(uuids)):
        account = {
            "id": str(uuid.uuid4()),
            "user_id": uuids[i],
            "credit_score": random.randint(300, 850),
            "updated": datetime.now().isoformat()
        }
        accounts.append(account)
    return accounts


def generate_credit_transactions(num_entries: int, ca_ids: list) -> list:
    transactions = []
    for i in range(num_entries):
        transaction = {
            "id": str(uuid.uuid4()),
            "account_id": random.choice(ca_ids),
            "amount": round(random.uniform(50, 5000), 2),
            "created": random_date(datetime.now() - timedelta(days=365), datetime.now()).isoformat(),
            "updated": datetime.now().isoformat()
        }
        transactions.append(transaction)
    return transactions
