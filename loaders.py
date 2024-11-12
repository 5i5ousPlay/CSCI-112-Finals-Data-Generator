from pymongo import MongoClient
from managers import EncryptionKeyManager


class DataLoader:
    hostname = None
    port = None
    uri = None
    client = None
    data = {}
    database = None
    encryption_key_path = None

    def __init__(self, hostname: str, database: str, data: dict, port=27017, encryption_key_path="encryption_key.key"):
        self.hostname = hostname
        self.port = port
        self.uri = f"mongodb://{hostname}:{port}/"
        self.database = database
        self.data = data
        self.encryption_key_path = encryption_key_path
        
    def validate_data(self, needed_fields: list[dict]):
        doc_str=['full_name','first_name','last_name', "middle_name", "valid_id_type",
                 "current_add", "permanent_add", ]
        
        if not isinstance(needed_fields, list):
            return "Invalid format: Expected a list"
        
        for item in needed_fields:
            for key, value in item.items():
                if key in doc_str:
                    if not isinstance(value, str):
                        return f"Invalid format: Field '{key}' should be a string but found {type(value).__name__}"
        

    def _connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.client.admin.command('ping')
            print("Connected to MongoDB!")
        except Exception as e:
            print("Failed to connect:", e)
            raise e
        
    def validate_data(self, needed_fields: list[dict]):
        doc_str = [
            "_id", "app_status",  "birth_date", "company_working",
            "current_add", "date_submitted", "email", "employment_status", "first_name",
            "full_name", "income_source", "job_title", "last_name", "middle_name",
            "mode", "notes", "payslip", "permanent_add", "phone_number", "self_picture",
            "tel_number", "updated", "user_profile", "valid_id_number", "valid_id_type"
        ]
        
        if not isinstance(needed_fields, list):
            return "Invalid format: Expected a list"
        
        for item in needed_fields: 
            if not isinstance(item, dict):
                return "Invalid format: Each item should be a dictionary"
            
            for key, value in item.items():
                if key in doc_str:
                    if not isinstance(value, str):
                        return f"Invalid format: Field '{key}' should be a string but found {type(value).__name__}"
                    if not value.strip():  
                        return f"Invalid format: Field '{key}' should not be empty"
        
        return "Validation successful"

    def _encrypt(self, collection_data: list[dict]):
        em = EncryptionKeyManager(self.encryption_key_path)
        encrypted_collection_data = []
        for item in collection_data:
            encrypted_item = {}
            for key, value in item.items():
                if key == '_id':
                    encrypted_item[key] = value
                else:
                    encrypted_item[key] = em.encrypt(value)
            encrypted_collection_data.append(encrypted_item)
        return encrypted_collection_data

    def _load(self):
        try:
            db = self.client[self.database]
            for collection_data in self.data:
                collection = db[collection_data]
                encrypted_collection_data = self._encrypt(self.data[collection_data])
                collection.insert_many(encrypted_collection_data)
                print(f"Inserted {len(encrypted_collection_data)} documents into {collection_data} collection")
        except Exception as e:
            raise e

    def start(self):
        try:
            self._connect()
            self._load()
        except Exception as e:
            raise RuntimeError(f"There was an error in loading the data: {str(e)}")
