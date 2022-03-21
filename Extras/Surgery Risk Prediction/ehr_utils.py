#!/usr/bin/python
import re
import numpy as np
import pandas as pd
import csv
import os 

from scipy import interp
from sklearn import metrics
from sklearn.metrics import precision_recall_curve, roc_curve, average_precision_score, brier_score_loss, make_scorer
from sklearn.metrics import auc, accuracy_score, roc_auc_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt


# helper functions for UCLA EHR project
# for questions contact brian.l.hill@cs.ucla.edu
data_dir="/data/DataNov21/"

# colours for plotting for BJA
COLOUR_1 = "#006BFA" # blue
COLOUR_2 = "#378E00" # green
COLOUR_3 = "#E64DFF" # pink
COLOUR_4 = "#FF8000" # gold
COLOUR_5 = "#33FFFF" # light blue
COLOUR_6 = "#FF3300" # orange
# uh-oh, ran out of choices...
COLOR_7 = 'black'
COLOR_8 = 'red'
COLOR_9 = 'silver'
PLOT_COLOURS = [COLOUR_1, COLOUR_2, COLOUR_3, COLOUR_4, COLOUR_5, COLOUR_6, COLOR_7, COLOR_8, COLOR_9]
# DPI for figures (for BJA, use 1200)
fig_dpi = 1200
# for figure text
label_text_size=16
legend_text_size=12
## added for grant plots
axis_text_size=2
#label_text_size=8
#legend_text_size=8
# default figure size
default_size=(8, 8)

from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)
import matplotlib as mpl
#mpl.rcParams['axes.linewidth'] = 0.25
#mpl.rcParams['font.sans-serif'] = "Helvetica"
# Then, "ALWAYS use sans-serif fonts"
#mpl.rcParams['font.family'] = "sans-serif"
#fontname="Helvetica"

def plot_roc_curve(models, model_names, model_probs, y_test, filename):
    plt.figure(figsize=default_size)
    lw = 2
    for i in range(len(model_names)):
        if isinstance(y_test, list):
            fpr, tpr, _ = roc_curve(np.array(y_test[i]), model_probs[i][:,1])
        else:
            fpr, tpr, _ = roc_curve(np.array(y_test), model_probs[i][:,1])
        roc_auc = auc(fpr, tpr)
        #plt.plot(fpr, tpr, PLOT_COLOURS[i], lw=lw, label=model_names[i]+' (AUC = %0.4f)' % roc_auc)
        plt.plot(fpr, tpr, PLOT_COLOURS[i], lw=lw, label=model_names[i])
    #plt.plot(fpr, tpr, color='darkorange',
    #         lw=lw, label='ROC curve (area = %0.4f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='black', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.yticks(np.arange(0., 1.1, 0.1))
    plt.xticks(np.arange(0., 1.1, 0.1))
    ax = plt.axes()
    # default width = 2, def length = 6
    ax.set_yticks(np.arange(0., 1.1, 0.1), minor=True)
    ax.set_xticks(np.arange(0., 1.1, 0.1), minor=True)
    ax.tick_params(direction='out', length=6, width=0.25, colors='black',labelsize=label_text_size)
    ax.tick_params(axis = 'both', which = 'minor', width=0.25)
    plt.xlabel('False Positive Rate', fontsize=label_text_size)
    plt.ylabel('True Positive Rate', fontsize=label_text_size)
    #plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right",fontsize=legend_text_size)
    plt.tight_layout()
    plt.savefig(filename, format="tif", dpi=fig_dpi)
    plt.show()


def plot_precision_recall_curve(models, model_names, model_probs, y_test, filename):
    #plt.figure(figsize=(7,7))
    plt.figure(figsize=default_size)
    for i in range(len(model_names)):
        if isinstance(y_test, list):
            precision, recall, thresholds = precision_recall_curve(np.array(y_test[i]), model_probs[i][:, 1])
        else:
            precision, recall, thresholds = precision_recall_curve(y_test, model_probs[i][:, 1])
        pr_auc = auc(recall, precision)
        #plt.step(recall, precision, PLOT_COLOURS[i], alpha=0.7,
        #     where='post', label=model_names[i]+' (AUC = %0.4f)' % pr_auc)
        plt.step(recall, precision, PLOT_COLOURS[i], alpha=0.7,
             where='post', label=model_names[i])
        plt.fill_between(recall, precision, step='post', alpha=0.2,
                     )

    plt.xlabel('Recall', fontsize=label_text_size)
    plt.ylabel('Precision', fontsize=label_text_size)
    plt.ylim([0.0, 1.05])
    plt.yticks(np.arange(0., 1.1, 0.1))
    ax = plt.axes()
    ax.tick_params(direction='out', length=6, width=0.25, colors='black', labelsize=label_text_size)
    ax.tick_params(axis = 'both', which = 'minor', width=0.25)
    ax.set_yticks(np.arange(0., 1.1, 0.1), minor=True)
    ax.set_xticks(np.arange(0., 1.1, 0.1), minor=True)
    plt.xlim([0.0, 1.05])
    plt.xticks(np.arange(0., 1.1, 0.1))
    #plt.title('Precision-Recall curve')
    plt.legend(loc="upper right", fontsize=legend_text_size)
    plt.tight_layout()
    plt.savefig(filename, format="tif", dpi=fig_dpi)
    plt.show()


def confusion_matrix_classification_rpt(models, model_names, model_predictions, y_test, dir_to_save_files):
    for i in range(len(model_names)):
#         precision, recall, f1, support = metrics.precision_recall_fscore_support(y_test, model_predictions[i], average='binary')
#         tn, fp, fn, tp = metrics.confusion_matrix(y_test, model_predictions[i]).ravel()
        print("==================================================")
        print("MODEL: ", model_names[i])
#         print "precision:\t", precision
#         print "recall:\t\t", recall
#         print "specificity:\t", float(tn) / (tn + fp)
#         print "F1:\t\t", f1
#         print "Support:\t", support
        print(confusion_matrix(y_test, model_predictions[i]))
        pd.DataFrame(confusion_matrix(y_test, model_predictions[i])).to_csv(
            os.path.join(dir_to_save_files, model_names[i].lower().replace(" ", "_") + "_confusion_matrix.txt"), sep='|', header=False, index=False)
#         print "TN:", tn, "FP:", fp, "FN:", fn, "TP:", tp
        print(classification_report(y_test, model_predictions[i], digits=4))

    
def plot_accuracy_roc_auc(models, model_names, model_predictions, model_probs, y_train, y_test, filename):
    # generate evaluation metrics
    model_acc = [accuracy_score(y_test, preds) for preds in model_predictions]
    model_roc_auc = [roc_auc_score(y_test, probs[:,1]) for probs in model_probs]
    model_avg_precision = [average_precision_score(y_test, probs[:,1]) for probs in model_probs]

    fig, ax = plt.subplots(figsize=default_size)
    index = np.arange(len(model_names))
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, model_acc, bar_width,
                     alpha=opacity,
                     color=PLOT_COLOURS[0],
                     label='Accuracy')

    rects2 = plt.bar(index + bar_width, model_roc_auc, bar_width,
                     alpha=opacity,
                     color=PLOT_COLOURS[1],
                     label='ROC AUC')
    
    rects3 = plt.bar(index + 2*bar_width, model_avg_precision, bar_width,
                     alpha=opacity,
                     color=PLOT_COLOURS[2],
                     label='Avg. Precision')

    plt.xlabel('Model')
    plt.ylabel('Score')
    plt.title('Model Accuracy/ROC AUC/Avg. Precision')
    plt.xticks(index + bar_width, model_names)
    plt.legend(loc="lower right")
    plt.gca().yaxis.grid(True)
    plt.ylim([0.0, 1.05])
    plt.plot([1.0 - y_train.mean()]*(len(models)), color=PLOT_COLOURS[3], lw=2, linestyle='--')
    plt.tight_layout()
    plt.savefig(filename, format="png", dpi=fig_dpi)
    plt.show()

    for i in range(len(model_names)):
        print(model_names[i], "Accuracy:\t\t", accuracy_score(y_test, model_predictions[i]))
        print(model_names[i], "ROC AUC:\t\t", roc_auc_score(y_test, model_probs[i][:, 1]))
        print(model_names[i], "Avg. Precision:\t\t", average_precision_score(y_test, model_probs[i][:, 1]))  

        
def plot_mean_square_error(models, model_names, mse):
    print("Mean Square Error:")
    for i in range(len(model_names)):
        print(model_names[i],"\t\t", mse[i])

    plt.figure(figsize=default_size)
    plt.gca().yaxis.grid(True)
    plt.bar(np.arange(len(models)), mse, align='center')
    plt.xticks(np.arange(len(models)), model_names)
    plt.xlabel('Classifier')
    plt.ylabel('Mean Square Error (MSE)')
    plt.title('Classifier MSE')
    plt.legend(loc="lower right")
    plt.show()        


def plot_cross_val_roc_curve(model_probs, y_test, filename):
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)

    i = 0
    for probs in model_probs:
        #probas_ = classifier.fit(X[train], y[train]).predict_proba(X[test])
        # Compute ROC curve and area the curve
        fpr, tpr, thresholds = roc_curve(y_test, probs[:, 1])
        tprs.append(interp(mean_fpr, fpr, tpr))
        tprs[-1][0] = 0.0
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        plt.plot(fpr, tpr, lw=1, alpha=0.3,
                 label='ROC fold %d (AUC = %0.3f)' % (i, roc_auc))

        i += 1
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
             label='Chance', alpha=.8)

    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    plt.plot(mean_fpr, mean_tpr, color='b',
             label=r'Mean ROC (AUC = %0.3f $\pm$ %0.3f)' % (mean_auc, std_auc),
             lw=2, alpha=.8)

    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + 2.*std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - 2.*std_tpr, 0)
    plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                     label=r'$\pm$ 2 std. dev.')

    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.yticks(np.arange(0., 1.1, 0.2))
    plt.xticks(np.arange(0., 1.1, 0.2))
    ax = plt.axes()
    # default width = 2, def length = 6
    ax.set_yticks(np.arange(0., 1.1, 0.1), minor=True)
    ax.set_xticks(np.arange(0., 1.1, 0.1), minor=True)
    ax.tick_params(direction='out', length=6, width=0.25, colors='black',labelsize=label_text_size)
    ax.tick_params(axis = 'both', which = 'minor', width=0.25)
    plt.xlabel('False Positive Rate', fontsize=label_text_size)
    plt.ylabel('True Positive Rate', fontsize=label_text_size)
    #plt.title('')
    plt.legend(loc="lower right")
    plt.savefig(filename, format="tif", dpi=fig_dpi)
    plt.show()    


def predict_given_threshold(probs, threshold=0.15):
    return [True if x[1] > threshold else False for x in probs]
    

def parse_etoh_col(etoh_string):
    #print etoh_string
    if etoh_string == '':
        return (None, None)
    try:
        u = [y.strip() for y in etoh_string.split("*")]
    except AttributeError:
        return (None, None)
    ynn = u[0].split(" ")[0]
    amt = u[1].split(":")[1]
    # get YES/NO/NA for ETOH use
    ynn_bool = True
    if ynn == 'NO': 
        ynn_bool = False
    elif ynn == 'NOT':
        ynn_bool = None
    # get amount (if available)
    amt_float = None
    try: 
        amt_float = float(amt)
    except:
        pass
    return (1 if ynn_bool else 0, amt_float)

def parse_smoking_col(smoke_string):
    #print smoke_string
    # if empty, return nothing
    if smoke_string == '':
        return (None, None, None)
    try:
        line = [i.strip() for i in smoke_string.split("*")]
    except AttributeError:
        return (None, None, None)
    # status = "NEVER SMOKER" or "FORMER SMOKER" or "CURRENT SMOKER"
    status = line[0]
    try:
        # get packs per day (PPD) and num years
        amount_length = line[1].split(" ")
    # if we don't have any PPD or YRS info, return what we do have
    except IndexError: 
        return (status, None, None)
    amt = None
    length = None
    amt, length = [i.split(":")[1] for i in amount_length]
    try:
        amt = float(amt)
    except ValueError:
        amt = None
    try:
        length = float(length)
    except ValueError:
        length = None
    #print status, amt, length
    return (status, amt, length)

# function for merging EF ranges (currently uses mean, but could use low, high, etc)
def merge_ef_range(ef_range):
    return str(int(np.mean([int(i) for i in ef_range.group(0).split('-')]))) 


def parse_last_ef_col(line):
    """
    Function for cleaning up data from the LAST_EF column
    
    returns tuple of EF values, where first element is EF 
    pre-exercise and second element is EF post-exercise
    """
    MIN_EF = 10
    MAX_EF = 100
    # remove all dates from string
    line = re.sub('([0-9]+[.\/])?[0-9]+[.\/][0-9]{2,4}\s', '', str(line))
    # remove any mention of time
    line = re.sub('[0-9]+\s?min[s]?', '', str(line))
    # remove any 20-- dates
    line = re.sub('20[0-9]+', '', str(line))
    # find all ranges (i.e. numeric separated by numeric via a dash; ex. 55-60)
    # and replace with merged value
    line = re.sub('\sto\s', '-', str(line))
    line = re.sub('[0-9]{2}-[0-9]{2}', merge_ef_range, str(line))
    #print line
    
    # get all numeric values from the string
    numeric_vals = re.findall('[0-9]{2}', line)
    numeric_vals = [int(i) for i in numeric_vals]
    # for each value in list, throw out if it's garbage (ex. date)
    for val in numeric_vals:
        if int(val) < MIN_EF or int(val) > MAX_EF:
            numeric_vals.remove(val)
    # if we have 1 value, return 
    if len(numeric_vals) == 1:
        return (numeric_vals[0], None)
    # if we have 2 values, 
    elif len(numeric_vals) == 2:
        return (numeric_vals[0], numeric_vals[1])
    # if we have 3 values, take first and third value (heuristically chosen)
    elif len(numeric_vals) == 3:
        return (numeric_vals[0], numeric_vals[2])
    # if we have 4 values, likely garbage in later two
    elif len(numeric_vals) == 4:
        return (numeric_vals[0], numeric_vals[1])
    # else not sure what we got, return nothing 
    else:
        return (None, None)


def create_icd10_ccs_map(ccs_icd_mapping_f):
    icd_ccs_map = {}
    with open(ccs_icd_mapping_f, 'r') as ccs_f:
            header = ccs_f.readline()
            for line in ccs_f:
                line = line.split(",")
                # map ICD10 CODE -> CSS CATEGORY
                icd_ccs_map[line[0]] = line[1]
    return icd_ccs_map

def get_ccs_vector():
    NUM_UNIQUE_CCS_CATEGORIES = 280
    main_f = os.path.join(data_dir, "Main_Data.txt")
    outcomes_f = os.path.join(data_dir, "Outcomes_Data.txt")
    icd_codes_f = os.path.join(data_dir, "ICD9_10Codes.txt")
    main_filtered_f = "Main_Data_filtered.txt"
    ccs_icd_mapping_f = "external_data/ccs_dx_icd10cm_2018_1.csv"

    # get mapping from ICD10 code to CCS category
    icd_ccs_map = create_icd10_ccs_map(ccs_icd_mapping_f)	

    with open(main_filtered_f, 'rb') as main_file:
        header = main_file.readline().split("\t")
        admsn_id_idx = header.idx("ADMSN_ID")

        # for each patient in main file
        for line in main:
            line = line.split("\t")
            # initialize vector to zero for categories
            ccs_cat_vec = np.zeros(NUM_UNIQUE_CCS_CATEGORIES)
            # create list to hold CCS categories for each patient
            ccs_list = []
            # get this patient's ADMSN_ID
            print(line)
            admsn_id = line[admsn_id_idx]

            with open(icd_codes_f) as icd_codes_file:
                icd_codes = csv.DictReader(icd_codes_file, delimiter="|")
                # find codes that match ADMSN_ID
                for l in icd_codes:
                    if l['ENCOUNTER_ID'] == admsn_id:
                        # map ICD10 code to CCS category
                        ccs_cat = icd_ccs_map[l['ICD-10-CM CODE']]
                        # add to list 
                        ccs_list.append(ccs_cat)
                # for each CCS category in our list, increment counter in feature vector
                # so that if we see a particular category multiple times, it has a higher
                # value in the feature vector than a cat we only see once
                print(admns_id, ccs_list)
                for cat in ccs_list:
                    ccs_cat_vec[int(cat)] += 1
                print(ccs_cat_vec)
                print("\n")



if __name__ == '__main__':
    get_ccs_vector()
