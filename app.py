import json
from flask import Flask, jsonify, request
from pymongo import MongoClient
from managers import EncryptionKeyManager
from helpers import CollectionGetter, CollectionPoster, CollectionDeleter, CollectionUpdater
from validation import DataValidator


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


@app.route("/retrieve/application/<string:item_id>/", methods=["GET"])
def get_application(item_id: str):
    application_getter = CollectionGetter(client=client, database=database, collection='applications',
                                          encryption_manager=em, is_encrypted=True)
    item = application_getter.handle_item(item_id=item_id)
    return item


@app.route('/create/application/', methods=['POST'])
def create_application():
    validator = DataValidator('schema')
    cp = CollectionPoster(client=client, database=database, collection='applications', data_validator=validator,
                          encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cp.handle_item(item=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to post item", "details": str(e)}), 500


@app.route('/update/application/<string:item_id>/', methods=['PATCH'])
def update_application(item_id:str):
    validator = DataValidator('schema', update=True)
    cu = CollectionUpdater(client=client, database=database, collection='applications', data_validator=validator,
                           encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cu.handle_item(item_id=item_id, data=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to update item", "details": str(e)}), 500


@app.route('/delete/application/<string:item_id>/', methods=['DELETE'])
def delete_application(item_id: str):
    cd = CollectionDeleter(client=client, database=database, collection='applications')
    result = cd.handle_item(item_id=item_id)
    return result


@app.route("/update/user_profiles/<string:item_id>", methods=['PATCH'])
def update_user_profile(item_id: str):
    validator = DataValidator('schema')
    cu = CollectionUpdater(client=client, database=database, collection='user_profiles', data_validator=validator,
                           encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cu.handle_item(item_id=item_id, data=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to update item", "details": str(e)}), 500


@app.route("/retrieve/user_profile/<string:item_id>/", methods=["GET"])
def get_user_profile(item_id: str):
    profile_getter = CollectionGetter(client=client, database=database, collection='user_profiles',
                                      encryption_manager=em, is_encrypted=True)
    item = profile_getter.handle_item(item_id=item_id)
    return item

