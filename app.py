import json
from flask import Flask, jsonify, request
from pymongo import MongoClient
from managers import EncryptionKeyManager
from helpers import CollectionGetter
from dataValidation import dataValidator


app = Flask(__name__)

try:
    with open('config.json', 'r') as f:
        config = json.load(f)

        hostname = config['hostname']
        port = config['port']
        database = config['database']
        n_applications = config['n_applications']
        credit_transaction_size = config['credit_transaction_size']
except Exception as e:
    raise e

client = MongoClient(f"mongodb://{hostname}:{port}/")
db = client[database]
em = EncryptionKeyManager('encryption_key.key')


@app.route("/get_application/<string:item_id>/", methods=["GET"])
def get_application(item_id: str):
    try:
        application_getter = CollectionGetter(client=client, database=database, collection='applications',
                                            encryption_manager=em, is_encrypted=True)
        item = application_getter.get_item(item_id=item_id)
        dataValidator.validate_application(item)
        return item
    except:
        return jsonify({"error": "Internal server error"})
        


@app.route("/get_user_profile/<string:item_id>/", methods=["GET"])
def get_user_profile(item_id: str):
    profile_getter = CollectionGetter(client=client, database=database, collection='user_profiles',
                                      encryption_manager=em, is_encrypted=True)
    item = profile_getter.get_item(item_id=item_id)
    return item
