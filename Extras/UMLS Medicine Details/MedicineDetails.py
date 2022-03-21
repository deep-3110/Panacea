

from urllib.request import urlopen
import pandas as pd
import json


def MedicineDetails(query):
    query=query.lower()
    query=query.replace(" ", "%20")
    url = "https://api.fda.gov/drug/label.json?search=purpose:"+query +"&limit=5"
    response = urlopen(url)
    data_json = json.loads(response.read())
    data_results=data_json['results']
    alldetailscombinedlist=[]
    for i in range(1,9):
       
        try:
            Keys=list(data_results[i].keys())
            Values=list(data_results[i].values())
            data_open_fda=data_results[i]['openfda']
            OpenFDAKeys=list(data_open_fda.keys())
            OpenFDAValues=list(data_open_fda.values())
            rxcui=OpenFDAValues[8][0]
            manufacturer_name=OpenFDAValues[3][0]
            generic_name=OpenFDAValues[2][0]
            purpose=Values[2][0]
            indications_and_usage=Values[16][0]
            dosage_and_administration=Values[10][0]
            route=OpenFDAValues[6][0]
            active_ingredient=Values[20][0]
            inactive_ingredient=Values[1][0]
            warnings=Values[4][0]
            product_type=OpenFDAValues[5][0]
            stop_use=Values[12][0]
            do_not_use=Values[14][0]
            ask_doctor_or_pharmacist=Values[19][0]
            alldetailscombinedlist.append(rxcui)
            alldetailscombinedlist.append(manufacturer_name)
            alldetailscombinedlist.append(generic_name)
            alldetailscombinedlist.append(purpose)
            alldetailscombinedlist.append(indications_and_usage)
            alldetailscombinedlist.append(dosage_and_administration)
            alldetailscombinedlist.append(route)
            alldetailscombinedlist.append(active_ingredient)
            alldetailscombinedlist.append(inactive_ingredient)
            alldetailscombinedlist.append(warnings)
            alldetailscombinedlist.append(product_type)
            alldetailscombinedlist.append(stop_use)
            alldetailscombinedlist.append(do_not_use)
            alldetailscombinedlist.append(ask_doctor_or_pharmacist)
            i+=1
        except:
            i+=2
       
    return(alldetailscombinedlist)

    print('--------------------------------')

MedicineList=MedicineDetails("Fever")
print(MedicineList)

