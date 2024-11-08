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

# Running the Program

The `main.py` file pulls the information from the `config.json` file, 
and allows you to specify how many applications to generate,
and how many credit card transaction records there will be.

To run the program simply run the following command in the terminal
of the project directory:

`python main.py`