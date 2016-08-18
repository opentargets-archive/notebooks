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
#ensGenes1 = utilityOT.read_genes_from_file('genelist_ens.txt')

## So this is my list of targets that are in ENS codes and we want to see what 
#evidence is out there in OT linking them to parkinson 
#myTargets = ensGenes1 #get first 10 of these

#PARKINSON_EFO = utilityOT.get_efoid('parkinson')
#NEURO_EFO = utilityOT.get_efoid('nervous system disease')

#And here is our evidence for Parkinson and for more general - nervous system disease 
#parkinsonTextCSV = utilityOT.get_disease_and_target_info('parkinson', myTargets, 'all')
#neuroTextCSV = utilityOT.get_disease_and_target_info('nervous system disease', myTargets, 'all')

#utilityOT.edit_header('parkinson_targets_all.csv')
#utilityOT.edit_header('nervous system disease_targets_all.csv')
#df = pd.read_csv(StringIO(parkinsonTextCSV),header=0,index_col=0)
df = pd.read_csv('disease_target_output/edited_header_parkinson_targets_all.csv',header=0,index_col=0)
print len(df.index)
print df



#dfall = pd.read_csv(StringIO(neuroTextCSV),header=0,index_col=0)
dfall = pd.read_csv('disease_target_output/edited_header_nervous system disease_targets_all.csv',header=0,index_col=0,)
print 'FOUND ' + str(len(dfall.index)) + ' Targets'
print dfall
#print df.count(value)

utilityOT.show_heatmap(df,8)
utilityOT.show_heatmap(dfall,8)

#Now lets get our files and extract first column into a list of targets
#print df.keys()
#print df.columns[0]
#print df.index
#targetNamesForDisease = df.index
#targetsForDisease = utilityOT.get_ens_genes(targetNamesForDisease)
#utilityOT.write_genes_to_file('disease_target_output/ENStargetsForParkinsons',targetsForDisease)


#print dfall.keys()
#print dfall.columns[0]
#print dfall.index
#targetNamesForTherapeuticArea = dfall.index
#targetsForTherapeuticArea = utilityOT.get_ens_genes(targetNamesForTherapeuticArea)
#utilityOT.write_genes_to_file('disease_target_output/ENStargetsForNSD',targetsForTherapeuticArea)

#Now lets go and get our evidence numbers for all the targets and disease 
#genetic_association = datasource.gwas + datasource.uniprot + datasource.eva
#uniprot+eva = mendelian


#targetsForDisease = utilityOT.read_genes_from_file('disease_target_output/ENStargetsForParkinsons')
targetsForTherapeuticArea = utilityOT.read_genes_from_file('disease_target_output/ENStargetsForNSD')

#And here is our evidence_counts for Parkinson and for more general - nervous system disease 
#parkinsonCountsTextCSV = utilityOT.get_disease_and_target_evidence_count('parkinson', targetsForDisease, 'counts')
neuroCountsTextCSV = utilityOT.get_disease_and_target_evidence_count('nervous system disease', targetsForTherapeuticArea, 'counts')

#utilityOT.edit_header('parkinson_targets_counts.csv',15)
utilityOT.edit_header('nervous system disease_targets_counts.csv',14)

#pdParkinson = pd.read_csv(StringIO(parkinsonCountsTextCSV),header=0,index_col=0)
#pdNeuro = pd.read_csv(StringIO(neuroCountsTextCSV),header=0,index_col=0)

dfParkinson = pd.read_csv('edited_header_parkinson_targets_counts.csv',header=0,index_col=0)
print dfParkinson;


dfParkinson['mendelian'] = dfParkinson.apply (lambda row: utilityOT.get_mendelian_count (row), axis=1)
print dfParkinson



dfNeuro = pd.read_csv('edited_header_nervous system disease_targets_counts.csv',header=0,index_col=0,)
print dfNeuro
dfNeuro['mendelian'] = dfNeuro.apply (lambda row: utilityOT.get_mendelian_count (row), axis=1)
print dfNeuro

#utilityOT.show_heatmap(dfParkinson, 14)
#utilityOT.show_heatmap(dfNeuro, 14)

print 'This is the end'















