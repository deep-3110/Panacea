from hashchain import records, ethereum
import json
from datetime import datetime
import random

# Set local JSON file as database
DATABASE = 'jsonDB.JSON'

with open(DATABASE) as file:
    dataset = json.load(file)

# Get inputs
ETH_PRIVATE_KEY = 'e9e1530ea75878a7016ebdd7ff91dd91ea4d7b293fa0ef5c4a064cb9cf1c23dc'
ETH_PUBLIC_KEY = '0x60577487A04B1DDa019565B883102457F27712Ec'
ETH_PROVIDER_URL = 'https://ropsten.infura.io/v3/9945375fabac486dba1b7c88b2d5f8e2'

# Get Eth contract interface. Deploy one if not existing
try:
    with open('contract_interface.JSON') as file:
        contract_interface = json.load(file)

except FileNotFoundError:
    print('Deploying contract ...')
    contract = ethereum.EthContract()
    contract.deploy(ETH_PUBLIC_KEY, ETH_PRIVATE_KEY, ETH_PROVIDER_URL)
    contract.get_txn_receipt()
    print('Contract deployed. Address: {}'.format(contract.address))

    contract_interface = dict(address=contract.address, abi=contract.abi)
    with open('contract_interface.JSON', 'w+') as file:
        json.dump(contract_interface, file)

# Build Ethereum connector
connector = ethereum.EthConnector(
    contract_abi=contract_interface['abi'],
    contract_address=contract_interface['address'],
    sender_public_key=ETH_PUBLIC_KEY,
    sender_private_key=ETH_PRIVATE_KEY,
    provider_url=ETH_PROVIDER_URL
)

# Verify database integrity
if records.verify(dataset[::-1]):
    key = 'ERDP-QT24'
    if dataset[-1]['hash'] != connector.get_record(key):
        raise ValueError('The hash registered on chain do not correspond to the last hash from the database')

doctor_name = input("Enter the Name of the Doctor - ")
patient_name = input("Enter the Patient Name - ")

# Build random data
data = {
    'timestamp': datetime.now().isoformat(),
    'sensorId': 'ERDP-QT24',  # dummy sensorId
    'value': random.random(),
    'doctorName': doctor_name,
    'patientName': patient_name
}

# Hash current data along with previous record hash to ensure integrity
try:
    last_record = dataset[-1]
    last_record_hash = last_record['hash']

except IndexError:  # If this is the first record in the DB
    last_record_hash = None

record = records.Record(data, last_record_hash)

# Save the record in the Smart Contract storage
key = 'ERDP-QT24'
transaction_hash = connector.record(key, record.get_hash())
print(transaction_hash)

# Add the record to the database
dataset.append(record.to_dict())

with open(DATABASE, 'w') as file:
    json.dump(dataset, file)