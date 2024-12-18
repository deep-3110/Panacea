from hashchain import records
import json
from datetime import datetime
import random

# Set local JSON file as database
DATABASE = 'jsonDB.json'

with open(DATABASE) as file:
    dataset = json.load(file)

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

# Add the record to the database
dataset.append(record.to_dict())

with open(DATABASE, 'w') as file:
    json.dump(dataset, file)