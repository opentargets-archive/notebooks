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


disease = "EFO_0000250"


print 'Hello World'

#assert utilityOT.symbol2ensemble('SOD1') == 'ENSG00000142168'
#assert utilityOT.get_ensid('SOD1') == 'ENSG00000142168'
#assert utilityOT.get_efoid('asthma') == 'EFO_0000270'

#utilityOT.get_all_gene_symbols()

#geneNames = utilityOT.read_genes_from_file()
#ensGenes  = utilityOT.get_ens_genes(geneNames)
#utilityOT.write_genes_to_file('genelist_ens.txt', ensGenes)

#These are Sanyals genes. 2 of them were not found - may be should look with the other 
#method, see if they turn up
ensGenes1 = utilityOT.read_genes_from_file('genelist_ens.txt')
myTargets = ensGenes1 #get first 10 of these

#PARKINSON_EFO = utilityOT.get_efoid('parkinson')
#NEURO_EFO = utilityOT.get_efoid('nervous system disease')

parkinsonTextCSV = utilityOT.get_disease_and_target_info('parkinson', myTargets)
neuroTextCSV = utilityOT.get_disease_and_target_info('nervous system disease', myTargets, 'all')

df = pd.read_csv(StringIO(parkinsonTextCSV),header=0,index_col=0)
df.head()

dfall = pd.read_csv(StringIO(neuroTextCSV),header=0,index_col=0)
dfall.head()















