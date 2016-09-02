import requests
import sys
import csv
import logging
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import json
from io import StringIO
import utilityOT
from collections import Counter
from operator import itemgetter
#gene_names_list = utilityOT.read_genes_from_file('/Users/rgaspary/GIT/CTTV/notebooks/blog/Literature/genelist_pd.txt')
#myTargets = utilityOT.get_ens_genes(gene_names_list, 'http://targetvalidation.org/api/latest/')
#utilityOT.write_genes_to_file('/Users/rgaspary/GIT/CTTV/notebooks/blog/Literature/gene_ens_codes.txt', myTargets)
#parkinsonCountsTextCSV = utilityOT.get_disease_and_target_evidence_count('parkinson', myTargets, '/Users/rgaspary/GIT/CTTV/notebooks/blog/Literature/parkinson_counts')
#myTargets = utilityOT.read_genes_from_file('/Users/rgaspary/GIT/CTTV/notebooks/blog/Literature/gene_ens_codes.txt')
#parkinsonLiteratureJson = utilityOT.get_literature_evidence('parkinson', myTargets, '/Users/rgaspary/GIT/CTTV/notebooks/blog/Literature/parkinson_counts_literature')

#utilityOT.edit_header('/Users/rgaspary/GIT/CTTV/notebooks/blog/Literature/parkinson_counts.csv', '/Users/rgaspary/GIT/CTTV/notebooks/blog/Literature/parkinson_counts_new_header.csv', 14)
#dfParkinson = pd.read_csv('/Users/rgaspary/GIT/CTTV/notebooks/blog/Literature/parkinson_counts_new_header.csv',header=0,index_col=0)
#dfParkinsonRows = len(dfParkinson.index)
#dfParkinsonSorted = dfParkinson.sort(['total','genetic_association',], ascending=[0,0])
#dfEvidenceTypes = dfParkinsonSorted.iloc[0:dfParkinsonRows, 0:8]
#print dfEvidenceTypes;

#dfPLit =  pd.read_json(StringIO(parkinsonLiteratureTextCSV),header=0,index_col=0)
#dfParkinsonLit = pd.read_json('/Users/rgaspary/GIT/CTTV/notebooks/blog/Literature/parkinson_counts_literature1.json')
#print dfParkinsonLit


targets= utilityOT.get_literature_breakdown('/Users/rgaspary/GIT/CTTV/notebooks/blog/Literature/', "n_counts_literature.json")
json_string = json.dumps(targets, indent=3)

#pandasObject = pd.read_json(json_string)

startEnd = utilityOT.format_json_for_visualization(targets, 'n_targets_literature_articles_visualization.json')
startYear = startEnd[0]
endYear = startEnd[1]
print "startYear = " +str(startEnd[0])
print "endYear = "+str(startEnd[1])
print 'This is the end, my friend'













