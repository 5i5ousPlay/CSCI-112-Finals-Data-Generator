from flask import jsonify
from pymongo import MongoClient
from managers import EncryptionKeyManager


class CollectionGetter:
    client = None
    collection = None
    database = None
    is_encrypted = False
    encryption_manager = None

    def __init__(self, client: MongoClient, database, collection: str, encryption_manager: EncryptionKeyManager,
                 is_encrypted=False):
        self.client = client
        self.database = self.client[database]
        self.collection = self.database[collection]
        self.is_encrypted = is_encrypted
        self.encryption_manager = encryption_manager

    def _decrypt_item(self, item:dict):
        encrypted_data = item
        encrypted_data_id = encrypted_data.pop("_id")
        try:
            decrypted_data = {"_id": encrypted_data_id}
            for key, value in encrypted_data.items():
                decrypted_data[key] = self.encryption_manager.decrypt(value)
        except Exception as e:
            return jsonify({"error": "Decryption failed", "details": str(e)}), 500

        return decrypted_data

    def get_item(self, item_id:str):
        item = self.collection.find_one({"_id": item_id})
        if self.is_encrypted:
            return self._decrypt_item(item)
        else:
            return item
