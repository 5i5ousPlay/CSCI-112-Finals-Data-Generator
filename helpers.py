from abc import ABC, abstractmethod
from flask import jsonify
from pymongo import MongoClient
from managers import EncryptionKeyManager


class CollectionHandler(ABC):
    client = None
    collection = None
    database = None

    def __init__(self, client: MongoClient, database: str, collection: str, encryption_manager=None,
                 is_encrypted=False):
        """
        Initialize the handler with a database, collection, and optional encryption manager.
        """
        self.client = client
        self.database = self.client[database]
        self.collection = self.database[collection]
        self.is_encrypted = is_encrypted
        self.encryption_manager = encryption_manager

    @abstractmethod
    def handle_item(self, *args, **kwargs):
        """
        Abstract method to handle an item.
        Must be implemented by subclasses.
        """
        pass

    def _decrypt_item(self, item: dict):
        """
        Decrypt an item if encryption is enabled.
        """
        if not self.is_encrypted or not self.encryption_manager:
            return item

        encrypted_data = item
        encrypted_data_id = encrypted_data.pop("_id")
        try:
            decrypted_data = {"_id": encrypted_data_id}
            for key, value in encrypted_data.items():
                decrypted_data[key] = self.encryption_manager.decrypt(value)
        except Exception as e:
            return jsonify({"error": "Decryption failed", "details": str(e)}), 500
        return decrypted_data


class CollectionGetter(CollectionHandler):
    def handle_item(self, item_id: str):
        item = self.collection.find_one({"_id": item_id})
        if self.is_encrypted:
            return self._decrypt_item(item)
        else:
            return item


class CollectionDeleter(CollectionHandler):
    def handle_item(self, item_id: str):
        try:
            self.collection.delete_one({"_id": item_id})
            return jsonify({"success": f"Deleted {item_id} from {self.collection.name}"})
        except Exception as e:
            return jsonify({"error": "Deletion failed", "details": str(e)}), 500

# class CollectionGetter:
#     client = None
#     collection = None
#     database = None
#     is_encrypted = False
#     encryption_manager = None
#
#     def __init__(self, client: MongoClient, database, collection: str, encryption_manager: EncryptionKeyManager,
#                  is_encrypted=False):
#         self.client = client
#         self.database = self.client[database]
#         self.collection = self.database[collection]
#         self.is_encrypted = is_encrypted
#         self.encryption_manager = encryption_manager
#
#     def _decrypt_item(self, item:dict):
#         encrypted_data = item
#         encrypted_data_id = encrypted_data.pop("_id")
#         try:
#             decrypted_data = {"_id": encrypted_data_id}
#             for key, value in encrypted_data.items():
#                 decrypted_data[key] = self.encryption_manager.decrypt(value)
#         except Exception as e:
#             return jsonify({"error": "Decryption failed", "details": str(e)}), 500
#
#         return decrypted_data
#
#     def get_item(self, item_id:str):
#         item = self.collection.find_one({"_id": item_id})
#         if self.is_encrypted:
#             return self._decrypt_item(item)
#         else:
#             return item


# class CollectionPoster:
#     client = None
#     collection = None
#     database = None
#     is_encrypted = False
#     encryption_manager = None
#
#     def __init__(self, client: MongoClient, database, collection: str, encryption_manager: EncryptionKeyManager,
#                  is_encrypted=False):
#         self.client = client
#         self.database = self.client[database]
#         self.collection = self.database[collection]
#         self.is_encrypted = is_encrypted
#         self.encryption_manager = encryption_manager
#


class CollectionDeleter:
    client = None
    collection = None
    database = None

    def __init__(self, client: MongoClient, database, collection: str):
        self.client = client
        self.database = self.client[database]
        self.collection = self.database[collection]

    def delete_item(self, item_id: str):
        try:
            self.collection.delete_one({"_id": item_id})
        except Exception as e:
            return jsonify({"error": "Deletion failed", "details": str(e)}), 500