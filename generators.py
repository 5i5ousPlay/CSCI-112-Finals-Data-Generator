import json
import os
from functions import *


class DataGenerator:
    n_applications = None
    credit_transaction_size = None
    uuids = {}
    output_dir = 'data'

    def __init__(self, n_applications, credit_transaction_size=20):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.n_applications = n_applications
        self.credit_transaction_size = credit_transaction_size
        self.uuids['applications'] = generate_uuids(num_ids=n_applications)
        self.uuids['users'] = generate_uuids(num_ids=n_applications)
        self.uuids['credit_accounts'] = generate_uuids(num_ids=random.randint(1, n_applications))

    def _generate_data(self) -> dict:
        data = {
            "user_profiles": generate_user_profile(uuids=self.uuids['users']),
            "applications": generate_application(uuids=self.uuids),
            "contact_info": generate_contact_info(num_entries=self.n_applications,
                                                  user_ids=self.uuids['users']),
            "banking_info": generate_banking_info(num_entries=self.n_applications,
                                                  application_ids=self.uuids['applications']),
            "financial_info": generate_financial_info(num_entries=self.n_applications,
                                                      application_ids=self.uuids['applications']),
            "credit_accounts": generate_credit_account(uuids=self.uuids['credit_accounts']),
            "credit_transactions": generate_credit_transactions(num_entries=self.credit_transaction_size,
                                                                ca_ids=self.uuids['credit_accounts'])
            }
        # user_profiles = generate_user_profile(uuids=self.uuids['users'])
        # applications = generate_application(uuids=self.uuids)
        return data
    
    def _load_data(self, data) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for collection in data:
            filename = f"{timestamp}_{collection}_data.json"
            path = os.path.join(self.output_dir, filename)
            with open(path, 'w+', encoding='utf-8') as f:
                json.dump(data[collection], f, ensure_ascii=False, indent=4)

    def start(self) -> dict:
        data = self._generate_data()

        self._load_data(data)

        return data
