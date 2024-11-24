import uuid
from abc import ABC, abstractmethod
from flask import jsonify
from pymongo import MongoClient


class CollectionHandler(ABC):
    """
    Abstract base class for handling MongoDB collections with optional data validation and encryption.

    Attributes:
        client (MongoClient): The MongoDB client.
        database (Database): The MongoDB database instance.
        collection (Collection): The MongoDB collection instance.
        data_validator (object): An optional data validator for validating input data.
        encryption_manager (object): An optional encryption manager for encrypting and decrypting data.
        is_encrypted (bool): Indicates if the data in the collection is encrypted.
    """

    client = None
    collection = None
    database = None
    data_validator = None

    def __init__(self, client: MongoClient, database: str, collection: str,
                 data_validator=None, encryption_manager=None,
                 is_encrypted=False):
        """
        Initialize the handler with a database, collection, and optional encryption manager.

        Args:
            client (MongoClient): The MongoDB client.
            database (str): The name of the database to connect to.
            collection (str): The name of the collection to manage.
            data_validator (object, optional): An object for validating data against schemas.
            encryption_manager (object, optional): An object for managing encryption and decryption.
            is_encrypted (bool, optional): Whether the collection data is encrypted. Defaults to False.
        """
        self.client = client
        self.database = self.client[database]
        self.collection_name = collection
        self.collection = self.database[collection]
        self.data_validator = data_validator
        self.is_encrypted = is_encrypted
        self.encryption_manager = encryption_manager


    @abstractmethod
    def handle_item(self, *args, **kwargs):
        """
        Abstract method for handling an item in the collection.

        Must be implemented by subclasses.
        """
        pass

    def _validate(self, data):
        """
        Placeholder for validation logic to be implemented by subclasses.

        Args:
            data (dict): The data to validate.
        """
        pass

    def _decrypt_item(self, item: dict):
        """
        Decrypt an item if encryption is enabled.

        Args:
            item (dict): The data item to decrypt.

        Returns:
            dict: The decrypted item, or the original item if decryption is not enabled.

        Raises:
            Exception: If decryption fails.
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
    """
    A class for inserting items into a MongoDB collection with optional validation and encryption.
    """

    def _validate(self, data):
        """
        Validate the given data against the collection schema.

        Args:
            data (dict): The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            Exception: If validation fails.
        """
        validated_data = data
        if self.data_validator is not None:
            try:
                self.data_validator.validate(data=validated_data, collection_name=self.collection_name)
            except Exception as e:
                raise e
            return validated_data
        else:
            return validated_data

    def handle_item(self, item: dict):
        """
        Insert an item into the collection.

        Args:
            item (dict): The data item to insert.

        Returns:
            tuple: A Flask JSON response and HTTP status code.
        """
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
    """
    A class for retrieving items from a MongoDB collection with optional decryption.
    """

    def handle_item(self, item_id: str):
        """
        Retrieve an item from the collection by its ID.

        Args:
            item_id (str): The ID of the item to retrieve.

        Returns:
            dict: The retrieved item, decrypted if necessary.
        """
        item = self.collection.find_one({"_id": item_id})
        if self.is_encrypted:
            return self._decrypt_item(item)
        else:
            return item


class CollectionUpdater(CollectionHandler):
    """
    A class for updating items in a MongoDB collection with optional validation and encryption.
    """

    def _validate(self, data):
        """
        Validate the given data against the collection schema.

        Args:
            data (dict): The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            Exception: If validation fails.
        """
        validated_data = data
        if self.data_validator is not None:
            try:
                self.data_validator.validate(data=validated_data, collection_name=self.collection_name)
            except Exception as e:
                raise e
            return validated_data
        else:
            return validated_data

    def handle_item(self, item_id:str, data: dict):
        """
        Update an item in the collection.

        Args:
            item_id (str): The ID of the item to update.
            data (dict): The new data for the item.

        Returns:
            tuple: A Flask JSON response and HTTP status code.
        """
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
    """
    A class for deleting items from a MongoDB collection.
    """

    def handle_item(self, item_id: str):
        """
        Delete an item from the collection by its ID.

        Args:
            item_id (str): The ID of the item to delete.

        Returns:
            tuple: A Flask JSON response and HTTP status code.
        """
        try:
            self.collection.delete_one({"_id": item_id})
            return jsonify({"success": f"Deleted {item_id} from {self.collection.name}"}), 204
        except Exception as e:
            return jsonify({"error": "Deletion failed", "details": str(e)}), 500
