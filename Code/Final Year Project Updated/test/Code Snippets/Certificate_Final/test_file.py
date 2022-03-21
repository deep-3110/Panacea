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
    print(f"The Dataset is \n{dataset}")
    print(f"The Key is \n{key}")
    if dataset[-1]['hash'] != connector.get_record(key):
        raise ValueError('The hash registered on chain do not correspond to the last hash from the database')

val_data = [{"doctorName": "James Bond", "patientName": "Carson Genna", "sensorId": "ERDP-QT24", "timestamp": "2022-01-08T22:44:16.208271", "value": 0.1378480046207523, "hash": "e6f78e2be1b2bebec4da9a9a93f6d3f0a958b0831d5683ac0db1a587fa609ba8", "previous_hash": "8ca7c23ccc0b9e540af9ba0dd32a0be44ceb0ddfe09299ab5976244fae63af95"}]

print(dataset)
print(type(dataset[0]))



if any(d['hash'] == val_data[0]['hash'] for d in dataset):
    print("The Data was Found")
else:
    print("The Data was Not Found")