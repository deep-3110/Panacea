from unicodedata import category
from flask import Flask, Response, render_template, request, redirect, url_for, jsonify
import sqlite3
#from hashchain import records, ethereum
import json
from datetime import datetime
import random
import ast
import hashlib
import pandas as pd
#import jwt
import requests
import json
from time import time
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
from csv import reader
import pandas as pd
import numpy as np
from collections import Counter
from pretty_html_table import build_table
import pdfkit
import codecs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders

app = Flask(__name__)


global p_careplans,p_conditions,p_devices,p_encounters,p_imaging_studies,p_immunizations,p_medications,p_observations,p_organizations,p_patients,p_payer_transitions,p_payers,p_procedures,p_providers
global p_careplans_list, p_conditions_list, p_encounters_list, p_imaging_studies_list, p_immunizations_list, p_medications_list, p_observations_list, p_procedures_list
global doctor_id, doctor_name
global requested_patient, requested_reason
global API_KEY, API_SEC
global patients_ex_df, patient_problems_ex_df, problems_from_notes_ex_df, problems_subject_id_list, indices, dataframe_problems, counter_df, proba_df, final_proba_df, problem_list, problems_list_unique, df2
global condition, drug_name, mean_pred
global text,category,confidenceScore

drug_df=pd.read_csv(r'test\dataset\drug-rec\grouped_drugRec.csv')
Name_list = drug_df["condition"].tolist()
conditions_list = list(set(Name_list))
def fetch_data(Patient_ID):
    global p_careplans,p_conditions,p_devices,p_encounters,p_imaging_studies,p_immunizations,p_medications,p_observations,p_organizations,p_patients,p_payer_transitions,p_payers,p_procedures,p_providers
    global p_careplans_list, p_conditions_list, p_encounters_list, p_imaging_studies_list, p_immunizations_list, p_medications_list, p_observations_list, p_procedures_list

    allergies=pd.read_csv(r'test\dataset\patients_data\synthetic-data\allergies.csv')
    careplans=pd.read_csv(r'test\dataset\patients_data\synthetic-data\careplans.csv')
    conditions=pd.read_csv(r'test\dataset\patients_data\synthetic-data\conditions.csv')
    devices=pd.read_csv(r'test\dataset\patients_data\synthetic-data\devices.csv')
    encounters=pd.read_csv(r'test\dataset\patients_data\synthetic-data\encounters.csv')
    imaging_studies=pd.read_csv(r'test\dataset\patients_data\synthetic-data\imaging_studies.csv')
    immunizations=pd.read_csv(r'test\dataset\patients_data\synthetic-data\immunizations.csv')
    medications=pd.read_csv(r'test\dataset\patients_data\synthetic-data\medications.csv')
    observations=pd.read_csv(r'test\dataset\patients_data\synthetic-data\observations.csv')
    organizations=pd.read_csv(r'test\dataset\patients_data\synthetic-data\organizations.csv')
    patients=pd.read_csv(r'test\dataset\patients_data\synthetic-data\patients.csv')
    payer_transitions=pd.read_csv(r'test\dataset\patients_data\synthetic-data\payer_transitions.csv')
    payers=pd.read_csv(r'test\dataset\patients_data\synthetic-data\payers.csv')
    procedures=pd.read_csv(r'test\dataset\patients_data\synthetic-data\procedures.csv')
    providers=pd.read_csv(r'test\dataset\patients_data\synthetic-data\providers.csv')
    supplies=pd.read_csv(r'test\dataset\patients_data\synthetic-data\supplies.csv')

    allergies=allergies.dropna()
    careplans=careplans.dropna()
    conditions=conditions.dropna()
    devices=devices.dropna()
    encounters=encounters.dropna()
    imaging_studies=imaging_studies.dropna()
    immunizations=immunizations.dropna()
    medications=medications.dropna()
    observations=observations.dropna()
    organizations=organizations.dropna()
    patients=patients.dropna()
    payer_transitions=payer_transitions.dropna()
    payers=payers.dropna()
    procedures=procedures.dropna()
    providers=providers.dropna()
    supplies=supplies.dropna()

    p_allergies=allergies.where(allergies.PATIENT == str(Patient_ID))
    p_careplans=careplans.where(careplans.PATIENT == str(Patient_ID))
    p_conditions=conditions.where(conditions.PATIENT == str(Patient_ID))
    p_devices=devices.where(devices.PATIENT==str(Patient_ID))
    p_encounters=encounters.where(encounters.PATIENT==str(Patient_ID))
    p_imaging_studies=imaging_studies.where(imaging_studies.PATIENT==str(Patient_ID))
    p_immunizations=immunizations.where(immunizations.PATIENT==str(Patient_ID))
    p_medications=medications.where(medications.PATIENT==str(Patient_ID))
    p_observations=observations.where(observations.PATIENT==str(Patient_ID))
    p_organizations=organizations.where(organizations.Id==str(Patient_ID))
    p_patients=patients.where(patients.Id==str(Patient_ID))
    p_payer_transitions=payer_transitions.where(payer_transitions.PATIENT==str(Patient_ID))
    p_payers=payers.where(payers.Id==str(Patient_ID))
    p_procedures=procedures.where(procedures.PATIENT==str(Patient_ID))
    p_providers=providers.where(providers.Id==str(Patient_ID))
    ############ DROPPING NaN Values ###############
    p_allergies=p_allergies.dropna()
    p_careplans=p_careplans.dropna()
    p_conditions=p_conditions.dropna()
    p_devices=p_devices.dropna()
    p_encounters=p_encounters.dropna()
    p_imaging_studies=p_imaging_studies.dropna()
    p_immunizations=p_immunizations.dropna()
    p_medications=p_medications.dropna()
    p_observations=p_observations.dropna()
    p_organizations=p_organizations.dropna()
    p_patients=p_patients.dropna()
    p_payer_transitions=p_payer_transitions.dropna()
    p_payers=p_payers.dropna()
    p_procedures=p_procedures.dropna()
    p_providers=p_providers.dropna()

    p_careplans_list = p_careplans[["START", "STOP", "DESCRIPTION", "REASONDESCRIPTION"]].values.tolist()
    p_conditions_list = p_conditions[["START", "STOP", "DESCRIPTION"]].values.tolist()
    p_encounters_list = p_encounters[["START", "STOP", "DESCRIPTION", "REASONDESCRIPTION"]].values.tolist()
    p_imaging_studies_list = p_imaging_studies[["BODYSITE_DESCRIPTION"]].values.tolist()
    p_immunizations_list = p_immunizations[["DATE", "DESCRIPTION"]].values.tolist()
    p_medications_list = p_medications[["START", "STOP", "DESCRIPTION", "REASONDESCRIPTION"]].values.tolist()
    p_observations_list = p_observations[["DATE", "DESCRIPTION", "VALUE", "UNITS"]].values.tolist()
    p_procedures_list = p_procedures[["DATE", "DESCRIPTION", "REASONDESCRIPTION"]].values.tolist()
    
    print(f"Procedures Value is - \n{p_procedures}")
    print(f"Procedures Value is - \n{p_procedures_list}")

def send_mail(name, email_id, doctor_name, date, time, meeting_link, meeting_password, doctor_email_id):
    # open file in read mode
    user_email = "panaceateam0@gmail.com"
    user_password = "nmims123"

    doctor_name = "James Bond"
    date = "11-02-2022"
    time = "10:00"

    print(email_id)
    print(name)

    #For Patient
    # html = Template(Path('index.html').read_text())
    html = Template(Path('email_template.html').read_text())
    email = EmailMessage()
    email['from'] = user_email
    email['subject'] = 'Appointment Confirmation'
    email['to'] = email_id
    email.set_content(html.substitute({'name': name, 'doctor_name': doctor_name, 'date': date, 'time': time, 'zoom_meeting_link': meeting_link, 'password': meeting_password}),'html')


    with smtplib.SMTP(host='smtp.gmail.com',port='587') as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(user_email,user_password) 
        smtp.send_message(email)
        print('Done!')

    #For Doctor
    html = Template(Path('email_template2.html').read_text())
    email = EmailMessage()
    email['from'] = user_email
    email['subject'] = 'Appointment Confirmation'
    email['to'] = doctor_email_id
    email.set_content(html.substitute({'name': name, 'doctor_name': doctor_name, 'date': date, 'time': time, 'zoom_meeting_link': meeting_link, 'password': meeting_password}),'html')


    with smtplib.SMTP(host='smtp.gmail.com',port='587') as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(user_email,user_password) 
        smtp.send_message(email)
        print('Done!')
    

def generate_meeting_link(name, email_id, doctor_name, date, appointment_time, doctor_email_id):
    global API_KEY, API_SEC

    # Enter your API key and your API secret
    API_KEY = 'SE61hgvwStGepPqmr9oZZw'
    API_SEC = 'CXsNKnR69n4JqUIQbj69TbfMxZMExVHukGJR'

    # create a function to generate a token
    # using the pyjwt library


    def generateToken():
        global API_KEY, API_SEC

        # Enter your API key and your API secret
        API_KEY = 'SE61hgvwStGepPqmr9oZZw'
        API_SEC = 'CXsNKnR69n4JqUIQbj69TbfMxZMExVHukGJR'

        # create a function to generate a token
        # using the pyjwt library
    
        token = jwt.encode(

            # Create a payload of the token containing
            # API Key & expiration time
            {'iss': API_KEY, 'exp': time() + 5000},

            # Secret used to generate token signature
            API_SEC,

            # Specify the hashing alg
            algorithm='HS256'
        )
        return token


    # create json data for post requests
    meetingdetails = {"topic": "The title of your zoom meeting",
                    "type": 2,
                    "start_time": "2019-06-14T10: 21: 57",
                    "duration": "45",
                    "timezone": "Europe/Madrid",
                    "agenda": "test",

                    "recurrence": {"type": 1,
                                    "repeat_interval": 1
                                    },
                    "settings": {"host_video": "true",
                                "participant_video": "true",
                                "join_before_host": "true",
                                "mute_upon_entry": "False",
                                "watermark": "true",
                                "audio": "voip",
                                "auto_recording": "cloud"
                                }
                    }

    # send a request with headers including
    # a token and meeting details


    def createMeeting():
        global API_KEY, API_SEC

        headers = {'authorization': 'Bearer ' + generateToken(),
                'content-type': 'application/json'}
        r = requests.post(f'https://api.zoom.us/v2/users/me/meetings', headers=headers, data=json.dumps(meetingdetails))

        print("creating zoom meeting ... ")
        # print(r.text)
        # converting the output into json and extracting the details
        y = json.loads(r.text)
        join_URL = y["join_url"]
        meeting_password = y["password"]

        print(f"here is your zoom meeting link {join_URL} and your password: {meeting_password}")
        send_mail(name, email_id, doctor_name, date, appointment_time, join_URL, meeting_password, doctor_email_id)

    # run the create meeting function
    createMeeting()

def mimic_test(cuid):
    global patients_ex_df, patient_problems_ex_df, problems_from_notes_ex_df, problems_subject_id_list, indices, dataframe_problems, counter_df, proba_df, final_proba_df, problem_list, problems_list_unique, df2
    
    patients_ex_df=pd.read_csv(r"test\dataset\mimic-data\PATIENT.csv")
    
    patient_problems_ex_df=pd.read_csv(r"test\dataset\mimic-data\patient_problems.csv")
    problems_from_notes_ex_df=pd.read_csv(r"test\dataset\mimic-data\problems_from_notes.csv")

    patients_ex_df=pd.read_csv(r"test\dataset\mimic-data\PATIENT.csv")
    
    df = patients_ex_df.where(patients_ex_df.SUBJECT_ID ==10144)
    
    patient_problems_ex_df=pd.read_csv(r"test\dataset\mimic-data\patient_problems.csv")
    
    df = patient_problems_ex_df.where(patient_problems_ex_df.description==cuid)

    df = df.dropna()

    list1 = df["cui"].values.tolist()

    print(list1)

    cuid = str(list1[0])
    
    problems_from_notes_ex_df=pd.read_csv(r"test\dataset\mimic-data\problems_from_notes.csv")
    
    problems_from_notes_ex_df.head()
    
    df = problems_from_notes_ex_df.where(problems_from_notes_ex_df.subject_id==10144)

    problems_id=problems_from_notes_ex_df.where(problems_from_notes_ex_df.problems==cuid).dropna()
    
    def unique(list1):
        x = np.array(list1)
        return(np.unique(x))

    problems_subject_id_list=problems_id['subject_id'].values.tolist()
    problems_subject_id_list=np.unique(problems_subject_id_list)
    indices = np.where(problems_subject_id_list==cuid)
    problems_subject_id_list = np.delete(problems_subject_id_list, indices)
    
    dataframe_problems=pd.DataFrame({"storetime":[],
                            "subject_id":[],
                                    "note_id":[],
                                    "problems":[],})
    df2=pd.DataFrame()
    for i in range(len(problems_subject_id_list[0:24])):
        df2=problems_from_notes_ex_df.where(problems_from_notes_ex_df.subject_id==problems_subject_id_list[i]).dropna()

        dataframe_problems=dataframe_problems.append(df2)
        i+=1
    
    problem_list=dataframe_problems['problems'].tolist()
    
    problems_list_unique=np.unique(problem_list)
    len(problem_list)

    unqiue_problem_list = list(dict.fromkeys(problems_list_unique))
    
    dataframe_problems_count=pd.DataFrame({"problems":[],
                            "count":[]})
    
    d=Counter(problem_list)
    
    counter_df = pd.DataFrame.from_dict(d, orient='index').reset_index()
    
    total=22488
    probability_list=[]
    cuid_list=counter_df['index'].tolist()
    counter_list=counter_df[0].tolist()
    for i in range(len(counter_list)):
        proba=(float(counter_list[i])/float(total))*100
        probability_list.append(str((round(proba, 4))))

    proba_df=pd.DataFrame({'cui':cuid_list,'Odds_Percentage':probability_list})

    final_proba_df=pd.merge(proba_df, patient_problems_ex_df, how ='inner', on ='cui')

    final_proba_df=final_proba_df.drop(['number'],axis=1)
    final_proba_df = final_proba_df.sort_values(['Odds_Percentage'], ascending=[False])
    final_proba_df.head()

    print(final_proba_df)
    final_proba_df.to_csv('Odds-Percentage-.csv')

      
    df = problems_from_notes_ex_df.where(problems_from_notes_ex_df.subject_id==10144)

    df=df.dropna()

    df2 =df.where(df.problems==cuid)

    df2=df2.dropna()
    print(df2)
    return df2

@app.route('/')
def home_page():
    return render_template('index.html')

def drugrec(medicine):
    global condition, drug_name, mean_pred

    drug_df=pd.read_csv(r'test\dataset\drug-rec\grouped_drugRec.csv')
    drug_df=drug_df.dropna()
    drug_df.head()
    p_drug_name=drug_df.where(drug_df.condition == medicine)
    p_drug_name=p_drug_name.sort_values(by=['mean'],ascending=False)
    condition=p_drug_name['condition'].dropna().values.tolist()
    drug_name=p_drug_name['drug_name'].dropna().values.tolist()
    mean_pred=p_drug_name['mean'].dropna().values.tolist()
    print('Drug Name: '+ str(drug_name[0:9]))
    print('\nCondition: '+ str(condition[0:9]))
    print('\nPrediction: '+ str(mean_pred[0:9]))

    condition = condition[0:9]
    drug_name = drug_name[0:9]
    mean_pred = mean_pred[0:9]

    return condition, drug_name, mean_pred

def index():
    return render_template('login_page.html')
    

@app.route('/certificate_validation')
def certificate_verification():

    source = request.args.get('value')
    print(f"The Value for Source is - {source}")
    print(type(source))
    source_list = ast.literal_eval(source)
    print(source_list)
    print(type(source_list))
    
    val_data = [{"doctorName": "James Bond", "patientName": "Carson Genna", "sensorId": "ERDP-QT24", "timestamp": "2022-01-08T22:44:16.208271", "value": 0.1378480046207523, "hash": "e6f78e2be1b2bebec4da9a9a93f6d3f0a958b0831d5683ac0db1a587fa609ba8", "previous_hash": "8ca7c23ccc0b9e540af9ba0dd32a0be44ceb0ddfe09299ab5976244fae63af95"}]
    # Set local JSON file as database
    DATABASE = 'test\dataset\json\jsonDB.json'

    with open(DATABASE) as file:
        dataset = json.load(file)

    # Get inputs
    ETH_PRIVATE_KEY = 'e9e1530ea75878a7016ebdd7ff91dd91ea4d7b293fa0ef5c4a064cb9cf1c23dc'
    ETH_PUBLIC_KEY = '0x60577487A04B1DDa019565B883102457F27712Ec'
    ETH_PROVIDER_URL = 'https://ropsten.infura.io/v3/9945375fabac486dba1b7c88b2d5f8e2'

    # Get Eth contract interface. Deploy one if not existing
    try:
        with open(r'test\dataset\json\contract_interface.JSON') as file:
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


    print(dataset)
    print(type(dataset[0]))



    if any(d['hash'] == dict(source_list[0])['hash'] for d in dataset):
        print("The Data was Found")
    else:
        print("The Data was Not Found")
    
    return render_template("New_Certificate_Validation.html", doctor_name = source_list[0]['doctorName'], patient_name = source_list[0]['patientName'], time_stamp = source_list[0]['timestamp'], hash = source_list[0]['hash'], value = source_list[0]['value'])

@app.route('/login_page')
def login_page():
    return render_template('login_page.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    global p_careplans,p_conditions,p_devices,p_encounters,p_imaging_studies,p_immunizations,p_medications,p_observations,p_organizations,p_patients,p_payer_transitions,p_payers,p_procedures,p_providers
    global p_careplans_list, p_conditions_list, p_encounters_list, p_imaging_studies_list, p_immunizations_list, p_medications_list, p_observations_list, p_procedures_list
    
    email_id = request.form["email_id"]
    password = request.form["password"]
    print(f"Email ID - {email_id} \n Password - {password}")

    con = sqlite3.connect(r'test\database\patient_login.db')
    
    cur = con.cursor()
    
    encoded = password.encode()
    result = hashlib.sha256(encoded).hexdigest()
    
    query = "SELECT COUNT(*) FROM PATIENT_LOGIN WHERE email_id = " + "'" + email_id + "'"
    
    for val in con.execute(query):
        check = val[0]
    
    print(query)
    
    if check == 1:
        query = "SELECT COUNT(*) FROM PATIENT_LOGIN WHERE email_id = " + "'" + email_id + "'" + "AND " + "password = " + "'" + result + "'"
        for val in con.execute(query):
            check = val[0]
        print(query)
        if check == 1:
            print("Successfully Logged In")

            con = sqlite3.connect(r'test\database\patient_login.db')
            cur = con.cursor()

            query = "SELECT data_id FROM PATIENT_LOGIN WHERE email_id = " + "'" + email_id + "'"
            for i in cur.execute(query):
                print(i[0])
                patient_id = i[0]

            con.commit()
            con.close()

            fetch_data(patient_id)
            print(f"Data Recieved is - \n{p_careplans_list}")
            #p_imaging_studies_list, p_immunizations_list, p_medications_list, p_observations_list, p_procedures_list
            
            return render_template('Patient_NER_new.html', conditions_val=conditions_list, careplans = p_careplans_list[0:5], conditions = p_conditions_list[0:5], encounters = p_encounters_list[0:5], imaging_studies_list = p_imaging_studies_list[0:5], immunizations_list = p_immunizations_list[0:5], medications_list = p_medications_list[0:5], observations_list = p_observations_list[0:5], procedures_list = p_procedures_list[0:5])
        elif check == 0:
            print("Incorrect Email ID or Password")
            return "Incorrect Email ID or Password"
    elif check == 0:
        print("User Does not Exist")
        return render_template('login_page.html')
        
#     print(check)
    
    con.commit()
    con.close()


    
@app.route('/patient_det', methods=["GET", "POST"])
def patient_det():
    patient_id='1d604da9-9a81-4ba9-80c2-de3375d59b40'    
    fetch_data(patient_id) 
    
    return render_template('Patient_details.html', careplans = p_careplans_list[0:5], conditions = p_conditions_list[0:5], encounters = p_encounters_list[0:5], imaging_studies_list = p_imaging_studies_list[0:5], immunizations_list = p_immunizations_list[0:5], medications_list = p_medications_list[0:5], observations_list = p_observations_list[0:5], procedures_list = p_procedures_list[0:5])
        
@app.route('/patient_dets', methods=["GET", "POST"])
def patient_dets():
    patient_id=request.form["process_text_val"]  
    fetch_data(patient_id) 
    
    return render_template('Patient_details.html', careplans = p_careplans_list[0:5], conditions = p_conditions_list[0:5], encounters = p_encounters_list[0:5], imaging_studies_list = p_imaging_studies_list[0:5], immunizations_list = p_immunizations_list[0:5], medications_list = p_medications_list[0:5], observations_list = p_observations_list[0:5], procedures_list = p_procedures_list[0:5])
        

@app.route('/patient_certificate', methods=["GET", "POST"])
def patient_certificate():
    con = sqlite3.connect(r'test\database\doctor_database.db')
    cur = con.cursor()

    doctor_first_name = []
    doctor_last_name = []

    # Create table
    query = "SELECT first_name, last_name FROM DOCTOR_DETAILS"
    for i in cur.execute(query):
        doctor_first_name.append(i[0])
        doctor_last_name.append(i[1])

    name = []
    for i in range(0, len(doctor_first_name)):
        name_val = doctor_first_name[i] + " " + doctor_last_name[i]
        name.append(name_val)
    print(name)
        
    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()
    return render_template("Patient_Certificate.html", name=name)       

@app.route('/request_certificate', methods=["GET", "POST"])
def request_certificate():
    doctor_name = request.form["doctor_name"]
    full_name = request.form["full_name"]
    requested_email_id = request.form["requested_email_id"]
    reason = request.form["reason"]

    print(doctor_name, full_name, requested_email_id, reason)

    con = sqlite3.connect(r'test\database\patient_login.db')
    cur = con.cursor()

    query = "SELECT id FROM PATIENT_LOGIN WHERE email_id = " + "'" + requested_email_id + "'"
    for i in cur.execute(query):
        patient_id = i[0]

    con.commit()

    con.close()

    con = sqlite3.connect(r'test\database\doctor_database.db')
    cur = con.cursor()

    for val in cur.execute('''SELECT id FROM CERTIFICATE_REQUEST WHERE id=(SELECT max(id) FROM CERTIFICATE_REQUEST)'''):
            id = val[0] + 1

    first_name = doctor_name.split(" ")

    query = "SELECT id FROM DOCTOR_DETAILS WHERE first_name = " + "'" + first_name[0] + "'"
    for i in cur.execute(query):
        doctor_id = i[0]
            
    query = "INSERT INTO CERTIFICATE_REQUEST VALUES (" + str(id) + "," + str(patient_id) + "," + "'" + full_name + "'" + "," + "'" + str(doctor_id) + "'" + "," + "'" + doctor_name + "'" + "," + "'" + reason + "'" + "," + "'" + requested_email_id + "'" + ")"
    cur.execute(query)


    con.commit()

    con.close()
    return render_template('Requested_Page.html')

@app.route('/doctor_login_page')
def doctor_login_page():
    return render_template('doctor_login_page.html')

@app.route('/doctor_login', methods=["GET", "POST"])
def doctor_login():
    global doctor_id

    email_id = "jamesbond@gmail.com"
    password = "12345678910"
    doctor_id = 1

    con = sqlite3.connect(r'test\database\doctor_database.db')
    cur = con.cursor()

    requested_patient_id = []
    requested_patient = []
    requested_patient_email_id = []

    # Create table
    query = "SELECT patient_id,patient_name, email_id FROM CERTIFICATE_REQUEST WHERE doctor_id = " + str(doctor_id)
    for i in cur.execute(query):
        requested_patient_id.append(i[0])
        requested_patient.append(i[1])
        requested_patient_email_id.append(i[2])

    print(requested_patient_id)
    print(requested_patient)
    print(requested_patient_email_id)
        
    con.commit()

    con.close()

    print(email_id, password, id)
    return render_template("Requested_Certificates.html", details = zip(requested_patient_id, requested_patient, requested_patient_email_id))

@app.route('/Patient_History.html', methods=["GET", "POST"])
def patient_history():
    return render_template("Patient_History.html")

@app.route('/Requested_Certificates.html', methods=["GET", "POST"])
def requested_certificates():
    global doctor_id
    
    return render_template("Requested_Certificates.html")

@app.route('/issue_certificate', methods=["GET", "POST"])
def issue_certificate():
    global doctor_id, doctor_name, requested_patient, requested_reason

    if request.method == "POST":
        patient_data = request.get_json()
        print(patient_data)

        patient_id = patient_data["id"]
        patient_name = patient_data["name"]
        patient_email_id = patient_data["email_id"]

        # patient_id = request.form["id"]
        # patient_name = request.form["name"]
        # patient_email_id = request.form["email_id"]

        con = sqlite3.connect(r'test\database\doctor_database.db')
        cur = con.cursor()

        doctor_id = 1

        requested_patient = []
        requested_reason = []

        # Create table
        query = "SELECT patient_name, reason FROM CERTIFICATE_REQUEST WHERE patient_id = " + str(patient_id) + " AND doctor_id = " + str(doctor_id)
        for i in cur.execute(query):
            requested_patient.append(i[0])
            requested_reason.append(i[1])

        requested_patient.append(patient_id)
        
        print(requested_patient)
        print(requested_reason)
            
        con.commit()

        con.close()

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'} 

        # return render_template("Doctor_Certificate.html", patient_name = requested_patient[0], reason = requested_reason[0])

@app.route('/render_issue_certificate', methods=["GET", "POST"])
def render_issue_certificate():
    global requested_patient, requested_reason
    
    print(requested_patient[0])
    print(requested_reason[0])

    return render_template("Doctor_Certificate.html", patient_name = requested_patient[0], reason = requested_reason[0])

@app.route('/doctor_certificate', methods=["GET", "POST"])
def doctor_certificate():
    return render_template("Doctor_Certificate.html")

@app.route('/create_certificate', methods=["GET", "POST"])
def create_certificate():
    global doctor_id, doctor_name, requested_patient
    
    print(f"Requested Patient - {requested_patient[1]}")
    patient_name = requested_patient[0]
    patient_id = requested_patient[-1]
    medical_condition = request.form["medical_condition"]
    severity = request.form["severity"]
    days_for_rest = request.form["days_for_rest"]

    print(f"Requested Patient - {requested_patient}")
    print(f"Medical Condition - {type(medical_condition)}")
    print(f"severity - {type(severity)}")
    print(f"days_for_rest - {type(days_for_rest)}")

    con = sqlite3.connect(r'test\database\doctor_database.db')
    cur = con.cursor()

    query = "SELECT doctor_name FROM CERTIFICATE_REQUEST WHERE doctor_id =" + str(doctor_id)

    for i in cur.execute(query):
        doctor_name = i[0]

    print(doctor_name)
    con.commit()

    con.close()

    print(patient_name, medical_condition, severity, days_for_rest)

    # Set local JSON file as database
    DATABASE = 'test\dataset\json\jsonDB.json'

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
    records.verify(dataset[::-1])

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
    
    con = sqlite3.connect(r'test\database\doctor_database.db')
    cur = con.cursor()

    for val in cur.execute('''SELECT id FROM ISSUED_CERTIFICATES WHERE id=(SELECT max(id) FROM ISSUED_CERTIFICATES)'''):
            id = val[0] + 1

    con.commit()

    con.close()

    con = sqlite3.connect(r'test\database\doctor_database.db')
    cur = con.cursor()

    doctor_id = 1
    
    val_dictionary = record.to_dict()
    hash = val_dictionary.get("hash")

    print(f"Dataset - {dataset}")
    print(f"Hash - {hash}, \n{type(hash)}")

    query = "INSERT INTO ISSUED_CERTIFICATES VALUES (" + str(id) + "," + "'" + patient_name + "'" + "," + str(doctor_id) + "," + "'" + doctor_name + "'" + "," + "'" + medical_condition + "'" + "," + "'" + severity + "'" + "," + "'" + days_for_rest + "'" + "," + "'" + hash + "')"

    cur.execute(query)

    con.commit()

    con.close()

    time_stamp = datetime.now().isoformat()
    dict_data = {"doctorName": doctor_name, "patientName": patient_name, "sensorId": "ERDP-QT24", "timestamp": datetime.now().isoformat(), "hash": hash}
    dict_data = list(dict_data)

    con = sqlite3.connect(r'test\database\doctor_database.db')
    cur = con.cursor()

    query = "DELETE FROM CERTIFICATE_REQUEST WHERE patient_id = " + str(patient_id)

    print(patient_id)

    cur.execute(query)

    con.commit()

    con.close()

    html_file=codecs.open("/Users/devdhawan/Desktop/Final Year Project Updated/test/templates/New_Certificate_Validation_PDF.html", 'r')
    # print(html.read())

    html = html_file.read()

    # html = str(html)
    print(type(html))

    html=html.replace("$patient_name",patient_name) 
    html=html.replace("$doctor_name",doctor_name)
    html=html.replace("$time_stamp",time_stamp)
    html=html.replace("$medical_condition",medical_condition)
    html=html.replace("$severity",severity)
    html=html.replace("$days_for_rest",days_for_rest)
    html=html.replace("$hash",hash)

    print(html)

    config = pdfkit.configuration(wkhtmltopdf = r"/Users/devdhawan/Desktop/Final Year Project Updated/test/wkhtmltox-0.12.6-2.macos-cocoa.pkg")  


    pdfkit.from_string(html, 'out.pdf')

    user_email = "panaceateam0@gmail.com"
    user_password = "nmims123"

    print(user_email)
    print(doctor_name)

    con = sqlite3.connect(r'test\database\patient_login.db')
    cur = con.cursor()

    query = "SELECT email_id FROM PATIENT_LOGIN WHERE id =" + str(patient_id)

    for i in cur.execute(query):
        patient_email_id = i[0]

    print(patient_email_id)
    con.commit()

    con.close()

    message_content = "Hello, Your Request for Certificate was approved by " + doctor_name + ". The Certificate has been attached in the mail."
    mail_content = message_content

    message = MIMEMultipart()
    message['From'] = user_email
    message['To'] = patient_email_id
    message['Subject'] = 'Certificate Generated'
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = '/Users/devdhawan/Desktop/Final Year Project Updated/test/out.pdf'
    attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    # message.attach(MIMEText(mail_content, "plain"))
    # Attach the pdf to the msg going by e-mail
    with open(attach_file_name, "rb") as f:
        #attach = email.mime.application.MIMEApplication(f.read(),_subtype="pdf")
        attach = MIMEApplication(f.read(),_subtype="pdf")
    attach.add_header('Content-Disposition','attachment',filename="Certificate.pdf")
    message.attach(attach)

    # message.attach(MIMEText(open(attach_file_name).read()))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(user_email, user_password) #login with mail_id and password
    text = message.as_string()
    session.sendmail(user_email, patient_email_id, text)
    session.quit()
    print('Mail Sent')

    return render_template("New_Certificate_Validation.html", doctor_name = doctor_name, patient_name = patient_name, time_stamp = time_stamp, medical_condition = medical_condition, severity = severity, days_for_rest = days_for_rest, hash = hash)

@app.route('/check_certificate_page', methods=["GET", "POST"])
def check_certificate_page():
    return render_template("Check_Certificate.html")

@app.route('/check_certificate', methods=["GET", "POST"])
def check_certificate():
    
    hash = request.form["hash"]
    DATABASE = 'test\dataset\json\jsonDB.JSON'

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


    print(dataset)
    print(type(dataset[0]))


    def value_find(S, x):
        for d in S:
            if d['hash'] == x:
                return d
        return False

    if any(d['hash'] == hash for d in dataset):
        print("The Data was Found")
        d = value_find(dataset, hash)
        print(f"The Value for d is - {d}")
        return render_template("Certificate_Found.html", hash=hash, patient_name=d['patientName'], doctor_name=d['doctorName'], time_stamp=d['timestamp'])
    else:
        print("The Data was Not Found")
        return render_template("Certificate_Not_Found.html")


@app.route('/create_appointment', methods=["GET", "POST"])
def create_appointment():
    con = sqlite3.connect(r'test\database\doctor_database.db')
    cur = con.cursor()

    doctor_first_name = []
    doctor_last_name = []

    # Create table
    query = "SELECT first_name, last_name FROM DOCTOR_DETAILS"
    for i in cur.execute(query):
        doctor_first_name.append(i[0])
        doctor_last_name.append(i[1])

    name = []
    for i in range(0, len(doctor_first_name)):
        name_val = doctor_first_name[i] + " " + doctor_last_name[i]
        name.append(name_val)
    print(name)
        
    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()
    return render_template("Create_Appointment.html", name=name)


@app.route('/request_appointment', methods=["GET", "POST"])
def request_appointment():
    doctor_name = request.form["doctor_name"]
    full_name = request.form["full_name"]
    requested_email_id = request.form["requested_email_id"]
    reason = request.form["reason"]
    date = request.form["scheduled_date"]
    time = request.form["scheduled_time"]

    print(doctor_name, full_name, requested_email_id, reason, date, time)

    con = sqlite3.connect(r'test\database\patient_login.db')
    cur = con.cursor()

    query = "SELECT id FROM PATIENT_LOGIN WHERE email_id = " + "'" + requested_email_id + "'"
    for i in cur.execute(query):
        patient_id = i[0]

    con.commit()

    con.close()

    con = sqlite3.connect(r'test\database\doctor_database.db')
    cur = con.cursor()

    first_name = doctor_name.split(" ")

    query = "SELECT id FROM DOCTOR_DETAILS WHERE first_name = " + "'" + first_name[0] + "'"
    for i in cur.execute(query):
        doctor_id = i[0]
    
    con.close()

    con = sqlite3.connect(r'test\database\appointment_database.db')
    cur = con.cursor()

    for val in cur.execute('''SELECT id FROM SCHEDULED_APPOINTMENTS WHERE id=(SELECT max(id) FROM SCHEDULED_APPOINTMENTS)'''):
            id = val[0] + 1

    query = "INSERT INTO SCHEDULED_APPOINTMENTS VALUES (" + str(id) + "," + str(patient_id) + "," + "'" + str(doctor_id) + "'" + "," + "'" + full_name + "'" + "," + "'" + doctor_name + "'" + "," +  "'" + date + "'" + "," + "'" + time + "'" + "," + "'" + reason + "'" + "," + "'" + requested_email_id + "'" + "," + "'" + "Requested" + "'" + ")"
    cur.execute(query)


    con.commit()

    con.close()
    return render_template("Requested_Page.html")


@app.route('/requested_appointments', methods=["GET", "POST"])
def requested_appointments():
    global doctor_id

    email_id = "jamesbond@gmail.com"
    password = "12345678910"
    doctor_id = 1

    con = sqlite3.connect(r'test\database\appointment_database.db')
    cur = con.cursor()

    requested_patient_id = []
    requested_patient = []
    requested_patient_email_id = []
    requested_patient_date = []
    requested_patient_time = []
    requested_patient_reason = []
    requested_patient_status = []

    # Create table
    query = "SELECT * FROM SCHEDULED_APPOINTMENTS WHERE doctor_id = " + str(doctor_id)
    for i in cur.execute(query):
        requested_patient_id.append(i[1])
        requested_patient.append(i[3])
        requested_patient_date.append(i[5])
        requested_patient_time.append(i[6])
        requested_patient_email_id.append(i[7])
        requested_patient_reason.append(i[8])
        requested_patient_status.append(i[9])

    print(requested_patient_id)
    print(requested_patient)
    print(requested_patient_date)
    print(requested_patient_time)
    print(requested_patient_email_id)
    print(requested_patient_reason)
    print(requested_patient_status)
        
    con.commit()

    con.close()

    print(email_id, password, id)
    return render_template("Requested_Appointments.html", details = zip(requested_patient_id, requested_patient, requested_patient_email_id, requested_patient_date, requested_patient_time, requested_patient_reason, requested_patient_status))


@app.route('/approve_appointment', methods=["GET", "POST"])
def approve_appointment():
    global doctor_name

    if request.method == "POST":
        patient_data = request.get_json()
        print(patient_data)
        patient_id = patient_data["patient_id"]
        name = patient_data["name"]
        email_id = patient_data["email_id"]
        doctor_name = "James Bond"
        date = patient_data["date"]
        time = patient_data["time"]
        doctor_email_id = "drjamesbond007@protonmail.com"
        print(name, email_id, doctor_name, date, time, doctor_email_id)
        generate_meeting_link(name, email_id, doctor_name, date, time, doctor_email_id)

        con = sqlite3.connect(r'test\database\appointment_database.db')
        cur = con.cursor()

        query = "DELETE FROM SCHEDULED_APPOINTMENTS WHERE patient_id = " + str(patient_id)

        cur.execute(query)

        con.commit()

        con.close()
        
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/search_disease', methods=["GET", "POST"])
def search_disease():
    return render_template("search_disease.html")

@app.route('/mimic_tables', methods=["GET", "POST"])
def mimic_tables():
    global df2

    cui = request.form["process_text_val"]
    mimic_test(cui)

    csv_file =pd.read_csv('Odds-Percentage-.csv')
    cui_list= csv_file["cui"]
    odds_percentage = csv_file["Odds_Percentage"]
    description = csv_file["description"]
    return render_template("predict_disease.html", mimic_list=zip(cui_list, odds_percentage, description))


@app.route('/drug_recommendation', methods=["GET", "POST"])
def drug_recommendation():
    global condition, drug_name, mean_pred

    medicine = request.get_data().decode('UTF-8')  
    medicine = medicine.replace('param=', '')
    postData = request.args.get('data')

    print(medicine)
    print(type(medicine))

    drugrec(str(medicine))
    
    # drug_list = jsonify({"list1": drug_name, "list2": mean_pred, "list3": condition})
    drug_list = list(zip(drug_name, condition, mean_pred))
    return jsonify({"list": drug_list})

@app.route('/process_text', methods=["GET", "POST"])
def process_text():
    medicine = request.get_data().decode('UTF-8')  
    medicine = medicine.replace('param=', '')
    medicine = medicine.replace('+', ' ')
    postData = request.args.get('data')

    myheader = {"Content-Type":"application/json"}
    print(myheader)
    mydata={"text":medicine}
    ##mydata="i have cough and cold. My heart rate is 93 bpm"
    print(mydata)
    api_url='https://prod-92.eastus.logic.azure.com:443/workflows/13e932579f28457d898c99e70f3fca3a/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=-GaClSwSHk5Cr2KL4nAVB8yQOmA7OTClbtqTCoriS68'
    print(api_url)
    response = requests.post(api_url, headers=myheader,json = mydata)
    print(response.json())

    updated_reponse = response.json()["results"]["documents"]
    print(updated_reponse)

    print(len(updated_reponse))

    global text
    global category
    global confidenceScore
    text = []
    category = []
    confidenceScore = []

    for i in updated_reponse:
        print(i)
        print(type(i))
        print(i["entities"])
        for j in i["entities"]:
            print(j["text"])
            print(j["category"])
            print(j["confidenceScore"])
            text.append(j["text"])
            category.append(j["category"])
            confidenceScore.append(j["confidenceScore"])

    print(text)
    print(category)
    print(confidenceScore)
    
    if len(text) >=5:
        text1 = text[0:5]
        category1 = category[0:5]
        confidenceScore1 = confidenceScore[0:5]
    elif len(text) < 5:
        for i in range(0, 5 - len(text)):
            text.append("")
            category.append("")
            confidenceScore.append("")
    
    text_list = list(zip(text1, category1, confidenceScore1))

    return jsonify({"text_list": text_list})

@app.route('/new_patient_ner', methods=["GET", "POST"])
def new_patient_ner():
    return render_template("Patient_NER_new.html")

@app.route('/ask_doctor', methods=["GET", "POST"])
def ask_doctor():
    con = sqlite3.connect(r'test\database\doctor_database.db')
    cur = con.cursor()

    doctor_first_name = []
    doctor_last_name = []

    # Create table
    query = "SELECT first_name, last_name FROM DOCTOR_DETAILS"
    for i in cur.execute(query):
        doctor_first_name.append(i[0])
        doctor_last_name.append(i[1])

    name = []
    for i in range(0, len(doctor_first_name)):
        name_val = doctor_first_name[i] + " " + doctor_last_name[i]
        name.append(name_val)
    print(name)
        
    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()
    return render_template("ask_doctor.html", name=name)

@app.route('/request_ask_doctor', methods=["GET", "POST"])
def request_ask_doctor():
    global patient_name
    
    reason = request.form["reason"]
    patient_name = request.form["full_name"]
    print('Request Doctor')

    print(text)
    print(category)
    print(confidenceScore)
    
    medicine = request.get_data().decode('UTF-8')  
    medicine = medicine.replace('param=', '')
    postData = request.args.get('data')

    print(medicine)
    print(type(medicine))

    drugrec(str(medicine))
    user_email = "panaceateam0@gmail.com"
    user_password = "nmims123"

    doctor_name = "James Bond"
    doctor_email_id = "drjamesbond007@protonmail.com"

    # #For Patient
    # # html = Template(Path('index.html').read_text())
    # email = EmailMessage()
    # email['from'] = user_email
    # email['subject'] = 'Opinion Requested by Mr/Mrs ' + patient_name
    # email['to'] = doctor_email_id
    # message = "Dr. " + doctor_name + "," + " Mr/Mrs. " + patient_name + " has requested your opinion for the following problem, " + "\n" + "Problem - " + reason + "\n" + "Text - " + str(text) + "\n" + "Category - " + str(category) + "\n" + "Confidence Score - " + str(confidenceScore)
    # email.set_content(message)


    # with smtplib.SMTP(host='smtp.gmail.com',port='587') as smtp:
    #     smtp.ehlo()
    #     smtp.starttls()
    #     smtp.login(user_email,user_password) 
    #     smtp.send_message(email)
    #     print('Done!')

    #For Patient
    # html = Template(Path('index.html').read_text())
    html = Template(Path('email_template3.html').read_text())
    email = EmailMessage()
    email['from'] = user_email
    email['subject'] = 'Opinion Requested by Mr/Mrs' + patient_name
    email['to'] = doctor_email_id

    df = pd.DataFrame(list(zip(text, category, confidenceScore)))

    df.columns =['Text', 'Category', 'Confidence Score']

    final_list = build_table(df, 'blue_light')

    print(final_list)

    email.set_content(html.substitute({'name': patient_name, 'doctor_name': doctor_name, 'problem': reason, 'final_list': final_list}),'html')


    with smtplib.SMTP(host='smtp.gmail.com',port='587') as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(user_email,user_password) 
        smtp.send_message(email)
        print('Done!')

    # #For Doctor
    # html = Template(Path('email_template2.html').read_text())
    # email = EmailMessage()
    # email['from'] = user_email
    # email['subject'] = 'Appointment Confirmation'
    # email['to'] = doctor_email_id
    # email.set_content(html.substitute({'name': name, 'doctor_name': doctor_name, 'date': date, 'time': time, 'zoom_meeting_link': meeting_link, 'password': meeting_password}),'html')


    # with smtplib.SMTP(host='smtp.gmail.com',port='587') as smtp:
    #     smtp.ehlo()
    #     smtp.starttls()
    #     smtp.login(user_email,user_password) 
    #     smtp.send_message(email)
    #     print('Done!')

    return render_template("Requested_Page.html")

@app.route('/predict_disease', methods=["GET", "POST"])
def predict_disease():
    return render_template("predict_disease.html")

if __name__ == "__main__":
    app.run(host = "localhost", debug = True)
    app.config["CACHE_TYPE"] = "null"