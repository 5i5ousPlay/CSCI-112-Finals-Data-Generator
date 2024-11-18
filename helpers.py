import uuid
from abc import ABC, abstractmethod
from flask import jsonify
from pymongo import MongoClient
from managers import EncryptionKeyManager
from validation import dataValidator


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

    def _validate(self, data):
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


class CollectionPoster(CollectionHandler):
    def _validate(self, data, schema_name):
        # TODO: Implement data validation for POST operations
        validator= dataValidator()
        try:
            validator.validate_data(data,schema_name)
        except:
            raise ValueError("Validation Error")
        
        validated_data = data
        return validated_data

    def handle_item(self, item: dict):
        validated_data = self._validate(item)
        if self.is_encrypted:
            encrypted_item = {}
            for key, value in validated_data.items():
                encrypted_item[key] = self.encryption_manager.encrypt(value)
            validated_data = encrypted_item

        validated_data['_id'] = str(uuid.uuid4())
        result = self.collection.insert_one(validated_data)
        db_item = self.collection.find_one(validated_data['_id'])
        return jsonify({"success": result.acknowledged, "item": self._decrypt_item(db_item)}), 201


class CollectionGetter(CollectionHandler):
    def handle_item(self, item_id: str):
        item = self.collection.find_one({"_id": item_id})
        if self.is_encrypted:
            return self._decrypt_item(item)
        else:
            return item


class CollectionUpdater(CollectionHandler):
    def _validate(self, data, schema_name):
        # TODO: Implement data validation for UPDATE operations
        validator= dataValidator()
        try:
            validator.validate_data(data,schema_name)
        except:
            raise ValueError("Validation Error")
        
        validated_data = data
        return validated_data

    def handle_item(self, item_id:str, data: dict):
        validated_data = self._validate(data=data)
        if self.is_encrypted:
            encrypted_data = {}
            for key, value in validated_data.items():
                encrypted_data[key] = self.encryption_manager.encrypt(value)
            result = self.collection.update_one({"_id": item_id}, {"$set": encrypted_data})
            item = self.collection.find_one({"_id": item_id})
            return jsonify({"success": result.acknowledged, "item": self._decrypt_item(item)}), 200
        else:
            result = self.collection.update_one({"_id": item_id}, {"$set": validated_data})
            item = self.collection.find_one({"_id": item_id})
            return jsonify({"success": result.acknowledged, "item": item}), 200


class CollectionDeleter(CollectionHandler):
    def handle_item(self, item_id: str):
        try:
            self.collection.delete_one({"_id": item_id})
            return jsonify({"success": f"Deleted {item_id} from {self.collection.name}"}), 204
        except Exception as e:
            return jsonify({"error": "Deletion failed", "details": str(e)}), 500
