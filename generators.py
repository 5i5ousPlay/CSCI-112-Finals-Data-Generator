import json
import os
from functions import *
from jsonschema import validate, ValidationError


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
    
    def validate_data(self, data: dict) -> None:
        schemas = {
            "user_profiles": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "gender": {"type": "string"}
                },
                "required": ["id", "name", "age", "gender"]
            },
            "applications": {
                "type": "object",
                "properties": {
                    "application_id": {"type": "string"},
                    "user_id": {"type": "string"},
                    "status": {"type": "string"}
                },
                "required": ["application_id", "user_id", "status"]
            },
        }

        for collection_name, items in data.items():
            schema = schemas.get(collection_name)
            if schema:
                for item in items:
                    try:
                        validate(instance=item, schema=schema)
                    except ValidationError as e:
                        raise ValueError(f"Validation failed for {collection_name}: {e.message}")

    def _validate_json_file(self, json_file: str, schemas: dict) -> None:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for collection_name, items in data.items():
            schema = schemas.get(collection_name)
            if schema:
                for item in items:
                    try:
                        validate(instance=item, schema=schema)
                    except ValidationError as e:
                        raise ValueError(f"Validation failed for {collection_name}: {e.message}")
        print(f"Data in {json_file} has been validated successfully.")
    
    def _load_data(self, data) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for collection in data:
            filename = f"{timestamp}_{collection}_data.json"
            path = os.path.join(self.output_dir, filename)
            with open(path, 'w+', encoding='utf-8') as f:
                json.dump(data[collection], f, ensure_ascii=False, indent=4)

    def start(self) -> dict:
        data = self._generate_data()
        
        schema=  {
            "type": "object",
            "properties": {
                "profiles": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "_id": {"type": "number"},
                            "full_name": {"type": "string"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "middle_name": {"type": "string"},
                            "birth_date": {"type": "string", "format": "date"},
                            "valid_id_type": {
                                "type": "string",
                                "enum": ["Passport", "Driver's License", "National ID"]
                            },
                            "valid_id_number": {"type": "string"},
                            "self_picture": {"type": "string", "format": "uri"},
                            "current_add": {"type": "string"},
                            "permanent_add": {"type": "string"},
                            "employment_status": {
                                "type": "string",
                                "enum": ["Employed", "Self-Employed", "Unemployed"]
                            },
                            "company_working": {"type": "string"},
                            "job_title": {"type": "string"},
                            "income_source": {
                                "type": "string",
                                "enum": ["Salary", "Business", "Investment", "Other"]
                            },
                            "payslip": {"type": "string"},
                            "updated": {"type": "string", "format": "date-time"}
                        },
                        "required": [
                            "_id","full_name", "birth_date","valid_id_type","valid_id_number", "current_add", "employment_status", "updated"
                        ]
                    }
                },
                "applications": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "_id": {"type": "string"},
                            "user_profile": {"type": "number"},
                            "date_submitted": {"type": "string", "format": "date-time"},
                            "app_status": {
                                "type": "string",
                                "enum": ["Pending", "Approved", "Rejected"]
                            },
                            "mode": {
                                "type": "string",
                                "enum": ["Online", "In-Person"]
                            },
                            "notes": {"type": "string"},
                            "apply_attempt": {"type": "integer"},
                            "updated": {"type": "string", "format": "date-time"}
                        },
                        "required": ["_id", "user_profile", "date_submitted", "app_status", "mode", "updated"]
                    }
                },
                "contact_info": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "_id": {"type": "string"},
                            "user_profile": {"type": "number"},
                            "email": {"type": "string", "format": "email"},
                            "phone_number": {"type": "string"},
                            "tel_number": {"type": "string"},
                            "updated": {"type": "string", "format": "date-time"}
                        },
                        "required": ["_id", "user_profile", "email", "phone_number", "updated"]
                    }
                },
                "banking_info": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "_id": {"type": "string"},
                            "application_id": {"type": "string"},
                            "bank_name": {"type": "string"},
                            "account_type": {
                                "type": "string",
                                "enum": ["Savings", "In-Checking"]
                            },
                            "account_number": {"type": "number"},
                            "bank_status": {
                                "type": "string",
                                "enum": ["Active", "Inactive"]
                            },
                        },
                        "required": ["_id", "application_id", "bank_name", "account_type", "account_number", "bank_status"]
                    }
                },
                "financial_info": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "_id": {"type": "string"},
                            "application_id": {"type": "string"},
                            "income": {"type": "number"},
                            "net_assets": {"type": "number"},
                            "net_debt": {"type": "number"},
                            "updated": {"type": "string", "format": "date-time"}
                        },
                        "required": ["_id", "application_id", "income", "net_assets", "net_debt", "updated"]
                    }
                },
                "credit_account": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "_id": {"type": "string"},
                            "user_id": {"type": "number"},
                            "credit_score": {"type": "integer"},
                            "updated": {"type": "string", "format": "date-time"}
                        },
                        "required": ["_id", "user_id", "credit_score", "updated"]
                    }
                },
                "credit_transactions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "_id": {"type": "string"},
                            "account_id": {"type": "string"},
                            "amount": {"type": "number"},
                            "created": {"type": "string", "format": "date-time"},
                            "updated": {"type": "string", "format": "date-time"}
                        },
                        "required": ["_id", "account_id", "amount", "created", "updated"]
                    }
                }
            },
            "required": ["applications", "contact_info", "banking_info", "financial_info", "credit_account", "credit_transactions"]
        }
        
        self._validate_json_file(data, schema)

        self._load_data(data)

        return data
