import spacy
import scispacy
import swifter
import pandas as pd
from spacy import displacy
import en_core_sci_sm
import en_core_sci_md
import en_ner_bc5cdr_md
import en_ner_jnlpba_md
import en_ner_craft_md
import en_ner_bionlp13cg_md
from collections import OrderedDict,Counter
from pprint import pprint
from tqdm import tqdm
tqdm.pandas()
from metapub import PubMedFetcher
from metapub import FindIt

def display_entities(model,document):
    nlp = model.load()
    doc = nlp(document)
    displacy_image = displacy.render(doc, jupyter=True,style='ent')
    entity_and_label = set([(X.text, X.label_) for X in doc.ents])
    return  displacy_image, entity_and_label
  
  
def PubMedFetcherquer(query):
    query=query
    fetch = PubMedFetcher()
    pmids = fetch.pmids_for_query(str(query), retmax=10)
    abstracts = []
    authorname=[]
    articletitle=[]
    url=[]
    for pmid in pmids:
        abstracts.append(fetch.article_by_pmid(pmid).abstract)
        authorname.append(fetch.article_by_pmid(pmid).authors)
        url.append(fetch.article_by_pmid(pmid).url)
        articletitle.append(fetch.article_by_pmid(pmid).title)
        #### RECOMMITED FROM HERE
    for i in range(len(abstracts)):
        sample_text=abstracts[i]
        #####
        bc5dr_entities = display_entities(en_ner_bc5cdr_md,sample_text)
        bc5dr_entities_dataframe = pd.DataFrame(bc5dr_entities[1],columns=['Entity','Label'])  #save returned values of entities and their labels in a pandas dataframe
        bc5dr_entities_dataframe['Ner_model'] = 'bc5dr'  #include a column with constant value of NER model
        bc5dr_entities_dataframe
        
        bionlp13cg_entities = display_entities(en_ner_bionlp13cg_md,sample_text)
        bionlp13cg_entities_dataframe = pd.DataFrame(bionlp13cg_entities[1],columns=['Entity','Label']) #save returned values of entities and their labels in a pandas dataframe
        bionlp13cg_entities_dataframe['Ner_model'] = 'bionlp13cg'  #include a column with constant value of NER model
        bionlp13cg_entities_dataframe
        
        craft_entities = display_entities(en_ner_craft_md,sample_text)
        craft_entities_dataframe = pd.DataFrame(craft_entities[1],columns=['Entity','Label'])  #save returned values of entities and their labels in a pandas dataframe
        craft_entities_dataframe['Ner_model'] = 'craft' #include a column with constant value of NER model
        craft_entities_dataframe
        jnlpba_entities = display_entities(en_ner_jnlpba_md,sample_text)
        jnlpa_entities_dataframe = pd.DataFrame(jnlpba_entities[1],columns=['Entity','Label']) #save returned values of entities and their labels in a pandas dataframe
        jnlpa_entities_dataframe['Ner_model'] = 'jnlpa' # include a column with constant value of NER model
        jnlpa_entities_dataframe
        entities_and_label_from_4_NER_model_dataframe = pd.concat([bc5dr_entities_dataframe,bionlp13cg_entities_dataframe,craft_entities_dataframe,jnlpa_entities_dataframe])
        entities_and_label_from_4_NER_model_dataframe.to_csv('entities_and_label_from_4_scispacy_NER_models.csv', index=False) #Save dataframe to csv
       
        entities_and_label_from_4_NER_model_dataframe = pd.read_csv('entities_and_label_from_4_scispacy_NER_models.csv')
        print(entities_and_label_from_4_NER_model_dataframe)
        
        
PubMedFetcherquer('breast neoplasm')
       
        
        
    
