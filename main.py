import json

from generators import DataGenerator
from loaders import DataLoader

if __name__ == '__main__':
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

    dg = DataGenerator(n_applications=n_applications, credit_transaction_size=credit_transaction_size)
    data = dg.start()

    dl = DataLoader(hostname=hostname, port=port, database=database, data=data)
    dl.start()
