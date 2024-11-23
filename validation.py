from jsonschema import validate, ValidationError
import json
import os


class DataValidator:
    """
    A class for validating data against JSON schemas stored in a specified directory.

    Attributes:
        schema_directory (str): The directory path where JSON schema files are stored.
    """
    schema_directory = None

    def __init__(self, schema_directory: str):
        """
        Initialize the DataValidator with the directory containing JSON schemas.

        Args:
            schema_directory (str): Path to the directory containing JSON schema files.
        """
        self.schema_directory = schema_directory

    def _load_schema(self, collection_name: str):
        """
        Load a JSON schema file for the specified collection.

        Args:
            collection_name (str): The name of the collection (used to locate the schema file).

        Returns:
           dict: The loaded JSON schema.

        Raises:
           ValueError: If the schema file does not exist in the specified directory.
        """
        schema_path = os.path.join(self.schema_directory, f"{collection_name}.json")
        if not os.path.exists(schema_path):
            raise ValueError(f"Schema file for {collection_name} does not exist at {schema_path}.")

        with open(schema_path, "r") as f:
            return json.load(f)

    def validate(self, data: dict, collection_name: str):
        """
        Validate the given data against the schema for the specified collection.

        Args:
            data (dict): The data to validate.
            collection_name (str): The name of the collection (used to locate the schema file).

        Raises:
            ValueError: If the data does not conform to the schema or if the schema file is invalid.
        """
        schema = self._load_schema(collection_name=collection_name)
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            raise ValueError(f"Validation failed for {collection_name}: {e.message}")
    