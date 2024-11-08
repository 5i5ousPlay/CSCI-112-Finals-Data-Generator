from pymongo import MongoClient


class DataLoader:
    hostname = None
    port = None
    uri = None
    client = None
    data = {}
    database = None

    def __init__(self, hostname: str, database: str, data: dict, port=27017):
        self.hostname = hostname
        self.port = port
        self.uri = f"mongodb://{hostname}:{port}/"
        self.database = database
        self.data = data

    def _connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.client.admin.command('ping')
            print("Connected to MongoDB!")
        except Exception as e:
            print("Failed to connect:", e)
            raise e

    def _load(self):
        try:
            db = self.client[self.database]
            for collection_data in self.data:
                collection = db[collection_data]
                collection.insert_many(self.data[collection_data])
                print(f"Inserted {len(self.data[collection_data])} documents into {collection_data} collection")
        except Exception as e:
            raise e

    def start(self):
        try:
            self._connect()
            self._load()
        except Exception as e:
            raise RuntimeError(f"There was an error in loading the data: {str(e)}")
