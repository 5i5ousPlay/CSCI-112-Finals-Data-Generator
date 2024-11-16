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

    def _connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.client.admin.command('ping')
            print("Connected to MongoDB!")
        except Exception as e:
            print("Failed to connect:", e)
            raise e
        

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
