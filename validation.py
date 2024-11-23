from jsonschema import validate, ValidationError
import json

class dataValidator:
  schema=  {
    "type": "object",
    "properties": {
        "user_profiles": {
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
        "credit_accounts": {
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
  
#when you post it will go through a validation class to check if the feilds are inside 
#required, 
  
  def validate_data(self, data: dict, schema_name: str) -> None:
    schema = self.schema["properties"].get(schema_name)
    if not schema:
        raise ValueError(f"No schema defined for {schema_name}")
    
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Validation failed for {schema_name}: {e.message}")
    