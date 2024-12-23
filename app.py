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


# ===========================APPLICATION CRUD==============================
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


# ===========================USER PROFILE CRUD==============================
@app.route('/create/user_profile/', methods =['POST'])
def create_user_profile():
    validator = DataValidator('schema')
    cp = CollectionPoster(client=client, database=database, collection='user_profiles', data_validator=validator,
                          encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cp.handle_item(item=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to post item", "details": str(e)}), 500


@app.route("/update/user_profile/<string:item_id>/", methods=['PATCH'])
def update_user_profile(item_id: str):
    validator = DataValidator('schema', update=True)
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


@app.route('/delete/user_profile/<string:item_id>/', methods=['DELETE'])
def delete_user_profile(item_id: str):
    cd = CollectionDeleter(client=client, database=database, collection='user_profiles')
    result = cd.handle_item(item_id=item_id)
    return result


# ===========================CONTACT INFO CRUD==============================
@app.route('/create/contact_info/', methods =['POST'])
def create_contact_info():
    validator = DataValidator('schema')
    cp = CollectionPoster(client=client, database=database, collection='contact_info', data_validator=validator,
                          encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cp.handle_item(item=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to post item", "details": str(e)}), 500


@app.route("/update/contact_info/<string:item_id>/", methods=['PATCH'])
def update_contact_info(item_id: str):
    validator = DataValidator('schema', update=True)
    cu = CollectionUpdater(client=client, database=database, collection='contact_info', data_validator=validator,
                           encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cu.handle_item(item_id=item_id, data=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to update item", "details": str(e)}), 500


@app.route("/retrieve/contact_info/<string:item_id>/", methods=["GET"])
def get_contact_info(item_id: str):
    profile_getter = CollectionGetter(client=client, database=database, collection='contact_info',
                                      encryption_manager=em, is_encrypted=True)
    item = profile_getter.handle_item(item_id=item_id)
    return item


@app.route('/delete/contact_info/<string:item_id>/', methods=['DELETE'])
def delete_contact_info(item_id: str):
    cd = CollectionDeleter(client=client, database=database, collection='contact_info')
    result = cd.handle_item(item_id=item_id)
    return result


# ===========================CONTACT INFO CRUD==============================
@app.route('/create/banking_info/', methods =['POST'])
def create_banking_info():
    validator = DataValidator('schema')
    cp = CollectionPoster(client=client, database=database, collection='banking_info', data_validator=validator,
                          encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cp.handle_item(item=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to post item", "details": str(e)}), 500


@app.route("/update/banking_info/<string:item_id>/", methods=['PATCH'])
def update_banking_info(item_id: str):
    validator = DataValidator('schema', update=True)
    cu = CollectionUpdater(client=client, database=database, collection='banking_info', data_validator=validator,
                           encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cu.handle_item(item_id=item_id, data=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to update item", "details": str(e)}), 500


@app.route("/retrieve/banking_info/<string:item_id>/", methods=["GET"])
def get_banking_info(item_id: str):
    profile_getter = CollectionGetter(client=client, database=database, collection='banking_info',
                                      encryption_manager=em, is_encrypted=True)
    item = profile_getter.handle_item(item_id=item_id)
    return item


@app.route('/delete/banking_info/<string:item_id>/', methods=['DELETE'])
def delete_banking_info(item_id: str):
    cd = CollectionDeleter(client=client, database=database, collection='banking_info')
    result = cd.handle_item(item_id=item_id)
    return result


# ===========================CREDIT ACCOUNTS CRUD==============================
@app.route('/create/credit_account/', methods =['POST'])
def create_credit_account():
    validator = DataValidator('schema')
    cp = CollectionPoster(client=client, database=database, collection='credit_accounts', data_validator=validator,
                          encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cp.handle_item(item=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to post item", "details": str(e)}), 500


@app.route("/update/credit_account/<string:item_id>/", methods=['PATCH'])
def update_credit_account(item_id: str):
    validator = DataValidator('schema', update=True)
    cu = CollectionUpdater(client=client, database=database, collection='credit_accounts', data_validator=validator,
                           encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cu.handle_item(item_id=item_id, data=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to update item", "details": str(e)}), 500


@app.route("/retrieve/credit_account/<string:item_id>/", methods=["GET"])
def get_credit_account(item_id: str):
    profile_getter = CollectionGetter(client=client, database=database, collection='credit_accounts',
                                      encryption_manager=em, is_encrypted=True)
    item = profile_getter.handle_item(item_id=item_id)
    return item


@app.route('/delete/credit_account/<string:item_id>/', methods=['DELETE'])
def delete_credit_account(item_id: str):
    cd = CollectionDeleter(client=client, database=database, collection='credit_accounts')
    result = cd.handle_item(item_id=item_id)
    return result


# ===========================CREDIT TRANSACTIONS CRUD==============================
@app.route('/create/credit_transaction/', methods =['POST'])
def create_credit_transaction():
    validator = DataValidator('schema')
    cp = CollectionPoster(client=client, database=database, collection='credit_transactions', data_validator=validator,
                          encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cp.handle_item(item=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to post item", "details": str(e)}), 500


@app.route("/update/credit_transaction/<string:item_id>/", methods=['PATCH'])
def update_credit_transaction(item_id: str):
    validator = DataValidator('schema', update=True)
    cu = CollectionUpdater(client=client, database=database, collection='credit_transactions', data_validator=validator,
                           encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cu.handle_item(item_id=item_id, data=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to update item", "details": str(e)}), 500


@app.route("/retrieve/credit_transaction/<string:item_id>/", methods=["GET"])
def get_credit_transaction(item_id: str):
    profile_getter = CollectionGetter(client=client, database=database, collection='credit_transactions',
                                      encryption_manager=em, is_encrypted=True)
    item = profile_getter.handle_item(item_id=item_id)
    return item


@app.route('/delete/credit_transaction/<string:item_id>/', methods=['DELETE'])
def delete_credit_transaction(item_id: str):
    cd = CollectionDeleter(client=client, database=database, collection='credit_transactions')
    result = cd.handle_item(item_id=item_id)
    return result

# ===========================FINANCIAL INFO CRUD==============================
@app.route('/create/financial_info/', methods =['POST'])
def create_financial_info():
    validator = DataValidator('schema')
    cp = CollectionPoster(client=client, database=database, collection='financial_info', data_validator=validator,
                          encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cp.handle_item(item=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to post item", "details": str(e)}), 500


@app.route("/update/financial_info/<string:item_id>/", methods=['PATCH'])
def update_financial_info(item_id: str):
    validator = DataValidator('schema', update=True)
    cu = CollectionUpdater(client=client, database=database, collection='financial_info', data_validator=validator,
                           encryption_manager=em, is_encrypted=True)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = cu.handle_item(item_id=item_id, data=data)
        return result
    except Exception as e:
        return jsonify({"error": "Failed to update item", "details": str(e)}), 500


@app.route("/retrieve/financial_info/<string:item_id>/", methods=["GET"])
def get_financial_info(item_id: str):
    profile_getter = CollectionGetter(client=client, database=database, collection='financial_info',
                                      encryption_manager=em, is_encrypted=True)
    item = profile_getter.handle_item(item_id=item_id)
    return item


@app.route('/delete/financial_info/<string:item_id>/', methods=['DELETE'])
def delete_financial_info(item_id: str):
    cd = CollectionDeleter(client=client, database=database, collection='financial_info')
    result = cd.handle_item(item_id=item_id)
    return result
