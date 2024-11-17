import json
from flask import Flask, jsonify, request
from pymongo import MongoClient
from managers import EncryptionKeyManager
from helpers import CollectionGetter, CollectionPoster


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
    cp = CollectionPoster(client=client, database=database, collection='applications', encryption_manager=em,
                     is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cp.handle_item(item=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to post item", "details": str(e)}), 500


@app.route("/retrieve/user_profile/<string:item_id>/", methods=["GET"])
def get_user_profile(item_id: str):
    profile_getter = CollectionGetter(client=client, database=database, collection='user_profiles',
                                      encryption_manager=em, is_encrypted=True)
    item = profile_getter.handle_item(item_id=item_id)
    return item



