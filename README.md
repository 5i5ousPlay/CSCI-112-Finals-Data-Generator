# Installing Dependencies

To install the necessary dependencies of the project run the 
following command

`pip install -r requirements.txt`

# Config File

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

# Running the Program

The `main.py` file pulls the information from the `config.json` file, 
and allows you to specify how many applications to generate,
and how many credit card transaction records there will be.

To run the program simply run the following command in the terminal
of the project directory:

`python main.py`