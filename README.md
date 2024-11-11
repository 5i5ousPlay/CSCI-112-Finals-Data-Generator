# Installing Dependencies

To install the necessary dependencies of the project run the 
following command

`pip install -r requirements.txt`

# Config File & AWS Setup

In order to run the program, you must have a `config.json` file specifying
the following necessary parameters (do not include the comments):

```json
{
  "hostname": "your_ec2_ipv4_address",
  "port": 27017, // default mongodb port change as necessary
  "database": "your database name",
  "n_applications": 50, // how many applications
  "credit_transaction_size": 300 // how many transactions
}
```

## AWS Setup

Make sure to configure your ec2 instance's security group to allow for 
TCP connections to the port your MongoDB server is listening in on 
(normally 27017) from your IP address (the My IP option). To confirm if the
ip address detected by AWS is correct, you can run the following command
in your terminal (Windows) to check:

`nslookup myip.opendns.com. resolver1.opendns.com`

Do not set this to 0.0.0.0 since this makes the server publicly available.

To get the hostname, simply copy the public ipv4 address found in 
the instance summery.

# Running the Data Generator & Loader

The `main.py` file pulls the information from the `config.json` file, 
and allows you to specify how many applications to generate,
and how many credit card transaction records there will be.

To run the program simply run the following command in the terminal
of the project directory:

`python main.py`

Running the `main.py` file will create a Data Generator instance that randomly
generates data for upload to the mongodb ec2 instance. A Data Loader instance
is also initialized and encrypts and loads the data from the Data Generator 
into the specified mongodb ec2 instance. To facilitate encryption, an
EncryptionKeyHandler is used within the Data Loader. 

**NOTE:** It is crucial that you do not lose your encryption key once the data
loader is ran, or else the encrypted data sent to the ec2 instance cannot
be decrypted or will be decrypted incorrectly.

## The Encryption Key Handler

This class handles the creation, loading, encryption, end decryption of information.
It accepts a path to an encryption key. If the encryption key does not exist, it
generates and saves a key `encryption_key.key` to the project directory. This
handler also allows for encrypting and decrypting information by wrapping 
the `cryptography` library's Fernet object.

# Starting the Demo Flask App

A simple flask app for demonstrating the decryption of encrypted information uploaded
to the ec2 instance is provided. To start the flask server, run the following command:

`flask --app app run`

To demonstrate the encryption and decryption, two API endpoints have been defined
in order to retrieve information from the `applications` and `user_profiles` 
collections respectively. 

To make API calls, you may use Postman or curl to the following endpoints:

```http request
http://127.0.0.1:5000/get_application/<your application id>/
http://127.0.0.1:5000/get_user_profile/<your user profile id>/
```

This will return the decrypted information from the server.

## Application

```json
{
    "_id": "adac24b4-0b7e-4cbc-b5b2-5bc5d32dda32",
    "app_status": "Rejected",
    "apply_attempt": "1",
    "date_submitted": "2023-03-21T15:07:16.456144",
    "mode": "Online",
    "notes": "Our fly big allow. Turn no there voice.",
    "updated": "2024-11-11T03:41:32.456144",
    "user_profile": "59c37849-53f5-4e01-a8bd-ce5281e16a9e"
}
```

## User Profile
```json
{
    "_id": "59c37849-53f5-4e01-a8bd-ce5281e16a9e",
    "birth_date": "1990-08-03",
    "company_working": "Kane-Vaughan",
    "current_add": "42640 Francisco Landing\nLake Justinstad, KS 42279",
    "employment_status": "Unemployed",
    "first_name": "Laura",
    "full_name": "Ernest Miller",
    "income_source": "Other",
    "job_title": "Teacher, special educational needs",
    "last_name": "Mccarthy",
    "middle_name": "Elizabeth",
    "payslip": "/fast/war.pdf",
    "permanent_add": "0177 Molina Turnpike\nWest Heatherport, IN 67847",
    "self_picture": "https://placekitten.com/811/798",
    "updated": "2024-11-11T03:41:32.360111",
    "valid_id_number": "514-27-0713",
    "valid_id_type": "National ID"
}
```