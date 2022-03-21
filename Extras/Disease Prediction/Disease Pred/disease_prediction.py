# Predicts diseases based on the symptoms entered and selected by the user.
#importing all necessary libraries
#!pip install xgboost
#!pip install googlesearch-python 
import warnings
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split, cross_val_score
from statistics import mean
from nltk.corpus import wordnet 
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from itertools import combinations
from time import time
from collections import Counter
import operator
from xgboost import XGBClassifier
import math
from sklearn.linear_model import LogisticRegression
import nltk
#nltk.download('all')
import re
from googlesearch import search
import warnings
import requests
from bs4 import BeautifulSoup

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
# returns the list of synonyms of the input word from thesaurus.com (https://www.thesaurus.com/) and wordnet (https://www.nltk.org/howto/wordnet.html)
'''def synonyms(term):
    synonyms = []
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.content,  "html.parser")
    try:
        container=soup.find('section', {'class': 'MainContentContainer'}) 
        row=container.find('div',{'class':'css-191l5o0-ClassicContentCard'})
        row = row.find_all('li')
        for x in row:
            synonyms.append(x.get_text())
    except:
        None
    for syn in wordnet.synsets(term):
        synonyms+=syn.lemma_names()
    return set(synonyms)
'''

def disease_predictor(final_symp):
    # utlities for pre-processing
    stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()
    splitter = RegexpTokenizer(r'\w+')
    df_comb = pd.read_csv("Dataset/dis_sym_dataset_comb.csv") # Disease combination
    df_norm = pd.read_csv("Dataset/dis_sym_dataset_norm.csv") # Individual Disease
    # Load Dataset scraped from NHP (https://www.nhp.gov.in/disease-a-z) & Wikipedia
    # Scrapping and creation of dataset csv is done in a separate program
    X = df_comb.iloc[:, 1:]
    Y = df_comb.iloc[:, 0:1]
    lr = LogisticRegression()
    lr = lr.fit(X, Y)
    scores = cross_val_score(lr, X, Y, cv=5)
    X = df_norm.iloc[:, 1:]
    Y = df_norm.iloc[:, 0:1]
    # List of symptoms
    dataset_symptoms = list(X.columns)
    # Create query vector based on symptoms selected by the user
    print("\nFinal list of Symptoms that will be used for prediction:")
    sample_x = [0 for x in range(0,len(dataset_symptoms))]
    for val in final_symp:
        print(val)
        sample_x[dataset_symptoms.index(val)]=1
    print(sample_x)
    # Predict disease
    lr = LogisticRegression()
    lr = lr.fit(X, Y)
    prediction = lr.predict_proba([sample_x])
    #Show top k diseases and their probabilities to the user.
    # K in this case is 10
    k = 10
    topk_dict = {}
    diseases = list(set(Y['label_dis']))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]
    
    print(f"\nTop {k} diseases predicted based on symptoms")
    diseasename=[]
    diseaseprobability=[]
    diseaseinfo=[]
    for idx,t in  enumerate(topk):
        match_sym=set()
        row = df_norm.loc[df_norm['label_dis'] == diseases[t]].values.tolist()
        row[0].pop(0)
        for idx,val in enumerate(row[0]):
            if val!=0:
                match_sym.add(dataset_symptoms[idx])
        prob = (len(match_sym.intersection(set(final_symp)))+1)/(len(set(final_symp))+1)
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key]*100
        print(str(j) + " Disease name:",diseases[key], "\tProbability:",str(round(prob, 2))+"%")
        diseasename.append(diseases[key])
        diseaseprobability.append(str(round(prob, 2)))
        topk_index_mapping[j] = key
        j += 1
        print(diseasename)
        print(diseaseprobability)
    for k in range(len(diseasename)):
        diseaseinfo.append(diseaseDetail(str(diseasename[k])))
        print(diseaseinfo)
        #print(diseaseDetail(dis))

    

def diseaseDetail(term):
    diseases=[term]
    ret=term+"\n"
    for dis in diseases:
        # search "disease wikipedia" on google 
        query = dis+' wikipedia'
        for sr in search(query,num_results=10): 
            # open wikipedia link
            match=re.search(r'wikipedia',sr)
            filled = 0
            if match:
                wiki = requests.get(sr,verify=False)
                soup = BeautifulSoup(wiki.content, 'html.parser')
                # Fetch HTML code for 'infobox'
                info_table = soup.find("table", {"class":"infobox"})
                if info_table is not None:
                    # Preprocess contents of infobox
                    for row in info_table.find_all("tr"):
                        data=row.find("th",{"scope":"row"})
                        if data is not None:
                            symptom=str(row.find("td"))
                            symptom = symptom.replace('.','')
                            symptom = symptom.replace(';',',')
                            symptom = symptom.replace('<b>','<b> \n')
                            symptom=re.sub(r'<a.*?>','',symptom) # Remove hyperlink
                            symptom=re.sub(r'</a>','',symptom) # Remove hyperlink
                            symptom=re.sub(r'<[^<]+?>',' ',symptom) # All the tags
                            symptom=re.sub(r'\[.*\]','',symptom) # Remove citation text                     
                            symptom=symptom.replace("&gt",">")
                            ret+=data.get_text()+" - "+symptom+"\n"
#                            print(data.get_text(),"-",symptom)
                            filled = 1
                if filled:
                    break
    return ret

# **Showing the list of top k diseases to the user with their prediction probabilities.**

# **For getting information about the suggested treatments, user can enter the corresponding index to know more details.**



final_symp = ['fever','headache','barky cough','belching','better sitting worse lying'] 
disease_predictor(final_symp)