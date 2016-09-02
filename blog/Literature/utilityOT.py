import requests
import json
import urllib
import gzip
import os.path
import random

import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

from collections import Counter
from operator import itemgetter
def symbol2ensemble(symbol):
    '''
    returns ensembl gene id for a gene symbol,
    leveraging the ensembl rest api
    '''
    headers = {'content-type':'application/json'}
    human_url = 'http://rest.ensembl.org/xrefs/symbol/homo_sapiens/'
    r = requests.get(human_url + symbol, headers=headers)
    return r.json()[0]['id']

def get_ensid(genesymbol, baseUrl='http://localhost:8008/api/latest/'):
    '''
    uses the targetvalidation.org API to get ENS IDs
    '''
    geneId=''
    r = requests.get(baseUrl + 'public/search', 
                     params={'q':genesymbol,'size':1,'filter':'gene'})
    if r.status_code == 200:
        result = r.json()
        if len(result["data"]) > 0:
            if result["data"][0]["data"]["approved_symbol"] == genesymbol:
                geneId = result["data"][0]["id"]
    else:
        print 'got status_code=' + str(r.status_code)
    #print 'genesymbol=' + genesymbol + ' geneId = ' +geneId
    return geneId


def get_efoid(diseasestr, baseUrl='http://localhost:8008/api/latest/'):
    '''
    uses the targetvalidation.org API to get EFO IDs
    '''
    
    r = requests.get(baseUrl + 'public/search', 
                     params={'q':diseasestr,'size':1,'filter':'disease'})
    result = r.json()
    diseaseId = result["data"][0]["data"]["efo_code"]
    return diseaseId

def search_disease(diseasestr,  baseUrl='http://localhost:8008/api/latest/'):
    '''
    create a diseasename.json file with results of the OT search
    '''    
   
    durl= baseUrl + 'public/search?size=10&from=0&q=' +diseasestr
    durlResponse=requests.get(durl)
    doutput=durlResponse.json()
    dJsonString = json.dumps(doutput, indent=2)
    f = open(diseasestr +'Search.json', 'w')
    f.write(dJsonString)
    print asthmaJsonString
    return None

'''
    Save all the genes in a file thePath + hgnc_symbol_set.txt'
'''
def get_all_gene_symbols(thePath=''):
    
    #first load the file with all gene info from EBI   
    if os.path.exists(thePath + 'hgnc_symbol_set.txt') == False:
        if os.path.exists(thePath + 'hgnc_complete_set.txt.gz') == False:
            url = 'http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc_complete_set.txt.gz'
            theFile = urllib.URLopener()
            theFile.retrieve(url, thePath + "hgnc_complete_set.txt.gz")
          
        #unzip it
        if os.path.isfile(thePath+'hgnc_complete_set.txt.gz'): 
            zippedFile = gzip.open(thePath+'hgnc_complete_set.txt.gz', 'rb')
            saveToFile = open(thePath+'hgnc_complete_set.txt', 'wb')
            saveToFile.write(zippedFile.read())
            
            zippedFile.close()
            saveToFile.close()
        
    #remove first line and then parse it and get second column
    readFrom = open(thePath+'hgnc_complete_set.txt', 'r')    
    writeTo = open(thePath+'hgnc_symbol_set.txt', 'w') 
    
    #Skip first line of the complete set - it is column names - dont need that
    theLine = readFrom.readline()
    while theLine != '':
        theLine = readFrom.readline()
        #print theLine
        #take second column
        theColumns = theLine.split("\t", 2)
        if len(theColumns) >=2:
            secondColumn =  theColumns[1]
        
            if secondColumn.endswith('withdrawn') == False:
                #print secondColumn
                writeTo.write(secondColumn + "\n")
    
    readFrom.close()
    writeTo.close()
    return None

def get_random_gene_names(filename='hgnc_symbol_set.txt', numGenes=10):
    #load all the lines in file into genes list, but strip newline/whitespace first
    with open(filename) as f:
        genes = [line.rstrip() for line in f] 
    random.shuffle(genes)
    #print(genes[:numGenes])
    #random_genes = [utilityOT.get_ensid(x) for x in genes[:numGenes] if get_ensid(x) is not None]
    random_genes = genes[:numGenes]
    #print random_genes
    return random_genes

'''
Take a list of genes and write them to a file one gene 
'''
def write_genes_to_file(fileName, genes):
    writeToFile = open(fileName, 'w');
    for gene in genes:
        writeToFile.write(gene+ '\n')
    return None

def read_genes_from_file(filename='genelist_pd.txt'):
    with open(filename) as f:
        genes = [line.rstrip() for line in f]
    
    return genes


'''
Take list of gene names and return a list of corresponding ENS gene codes
'''
def get_ens_genes(geneNames, baseUrl='http://localhost:8008/api/latest/'):
    ens_genes = []
    for x in geneNames: 
        ensid = get_ensid(x, baseUrl) 
        if ensid is not None:
            ens_genes.append(ensid)   
    return ens_genes

def get_disease_info(disease, baseUrl='http://localhost:8008/api/latest/'):
    disease_efo = get_efoid(disease, baseUrl)
    
    disease_csv = {'disease':disease_efo,
          'outputstructure':'flat',
          'facets':'false',
          'format':'csv',
          'size':'10000',
          'fields':['target.gene_info.symbol',
                    'association_score.overall',
                    'association_score.datatypes.genetic_association',
                    'association_score.datatypes.somatic_mutation',
                    'association_score.datatypes.known_drug',
                    'association_score.datatypes.affected_pathway',
                    'association_score.datatypes.rna_expression',
                    'association_score.datatypes.literature',
                    'association_score.datatypes.animal_model',
                    'target.gene_info.name'],
          'from':'0',
          'scorevalue_min':'0'
          }
    r = requests.get(baseUrl + 'public/association/filter', params = disease_csv)
    
    diseaseResults = open(disease + '.csv','w')
    diseaseResults.write(r.text)
    diseaseResults.close()
    
    return r.text

def get_disease_and_target_info(disease,targets,fileName='',baseUrl='http://localhost:8008/api/latest/'):
    disease_efo = get_efoid(disease, baseUrl)
    
    disease_csv = {'disease':disease_efo,
                   'target':targets,
          'outputstructure':'flat',
          'facets':'false',
          'format':'csv',
          'size':'10000',
          'fields':['target.gene_info.symbol',
                    'association_score.overall',
                    'association_score.datatypes.genetic_association',
                    'association_score.datatypes.somatic_mutation',
                    'association_score.datatypes.known_drug',
                    'association_score.datatypes.affected_pathway',
                    'association_score.datatypes.rna_expression',
                    'association_score.datatypes.literature',
                    'association_score.datatypes.animal_model',
                    'target.gene_info.name'],
          'from':'0',
          'scorevalue_min':'0'
          }
    r = requests.get(baseUrl + 'public/association/filter', params = disease_csv)
    if r.status_code == 200:
        diseaseResults = open(disease + '_targets_'+ fileName+ '.csv','w')
        diseaseResults.write(r.text)
        diseaseResults.close()
    
    return r.text

def get_disease_and_target_evidence_count(disease,targets,fileName='disease_target_count',baseUrl='http://localhost:8008/api/latest/'):
    disease_efo = get_efoid(disease, baseUrl)
    
    disease_csv = {'disease':disease_efo,
                   'target':targets,
          'outputstructure':'flat',
          'facets':'false',
          'format':'csv',
          'size':'10000',
          'fields':['target.gene_info.symbol',
                    'evidence_count.total',
                    'evidence_count.datatypes.genetic_association',
                    'evidence_count.datatypes.somatic_mutation',
                    'evidence_count.datatypes.known_drug',
                    'evidence_count.datatypes.affected_pathway',
                    'evidence_count.datatypes.rna_expression',
                    'evidence_count.datatypes.literature',
                    'evidence_count.datatypes.animal_model',
                    'evidence_count.datasources.gwas_catalog',
                    'evidence_count.datasources.eva',
                    'evidence_count.datasources.eva_somatic',
                    'evidence_count.datasources.uniprot',
                    'evidence_count.datasources.uniprot_literature'],
          'from':'0',
          'scorevalue_min':'0'
          }
    r = requests.get(baseUrl + 'public/association/filter', params = disease_csv)
    print "response status_code = " +str( r.status_code)
    if r.status_code == 200: 
        diseaseResults = open(fileName+'.csv','w')
        diseaseResults.write(r.text)
        diseaseResults.close()
    else: 
        print r.text
    return r.text

#http://localhost:8008/api/latest/public/evidence/filter?target=ENSG00000113580&disease=EFO_0000270&size=200&datasource=europepmc&expandefo=true
def get_literature_evidence(disease,targets,fileName='disease_target_evidence',baseUrl='http://localhost:8008/api/latest/'):
    disease_efo = get_efoid(disease, baseUrl)
    
    disease_csv = {'disease':disease_efo,
                   'target':targets,
                   'datasource':'europepmc',
                   'datastructure':'full',
          'outputstructure':'flat',
          'facets':'true',
          'size':'10000',          
          'from':'0',
          'scorevalue_min':'0'
          }
    r = requests.get(baseUrl + 'public/evidence/filter', params = disease_csv)
    print "response status_code = " +str( r.status_code)
    if r.status_code == 200: 
        diseaseResults = open(fileName+'.json','w')
        diseaseResults.write(r.text)
        diseaseResults.close()
    else: 
        print r.text
    return r.json()

def get_mendelian_count (row):
    mendelian = row['uniprot'] + row['uniprot_literature'] + row['eva'] + row['eva_somatic']
    return mendelian

def print_csv_table():
    

    '''
    Show data Frame as heatmap
    '''
def show_heatmap(df, columns, height=5):
    #Show heatmap for the df for parkinsonTextCSV
    # copying from Theo.. 
    f, ax = plt.subplots(figsize=(columns,height)) #figsize(x,y) - are in inchs
    #ax = sns.heatmap(df.iloc[:columns,0:columns], cmap="Blues", annot=True, linewidths=2)
    ax = sns.heatmap(df, cmap="Blues", annot=True, fmt='g', linewidths=2)
    # fix labels
    #labels = [item.get_text().split('.')[-1] for item in ax.get_xticklabels()]
    #labels = [item.get_text().split('.')[-1] for item in ax.get_xticklabels()]
    #t = ax.set_xticklabels(labels)
    #print "DONE"
    return None

def edit_header(fileNameFrom, fileNameTo, numColumns):
    readFrom = open(fileNameFrom, 'r')    
    writeTo = open( fileNameTo, 'w+')
     
    theLine = readFrom.readline()
    theColumns = theLine.split(",", numColumns)
    labels = [item.split('.')[-1] for item in theColumns]
    newEditedLine = ",".join( labels )
    print newEditedLine
    writeTo.write(newEditedLine);
    while theLine != '':
        theLine = readFrom.readline()
        #theColumns = theLine.split(",", numColumns)
        #numericColumns = theColumns[1:numColumns]
        #myValues=[theColumns[0]]; 
        #for item in numericColumns:
        #    myIntValue = int(float(item))
        #    myValues.append(str(myIntValue))
        #newEditedLine = ",".join( myValues ) 
        #print theLine
        #writeTo.write(newEditedLine + '\n')
        writeTo.write(theLine)
    readFrom.close()
    writeTo.close()    
    return None


def get_abstracts(query, targetName, fileName):
    baseUrl ='http://localhost:8000/proxy/www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resulttype=core&query=' + query
    result = None
    r = requests.get(baseUrl)
    #print "response status_code = " + str(r.status_code)
    if r.status_code == 200:
        abstractResults = open(fileName, 'w')
        r.encoding = "UTF-8"
        try:
            abstractResults.write(r.text)
        except UnicodeEncodeError:
            pass
            #print "UnicodeEncodeError for targetName=" + targetName + " query=" + query
        abstractResults.close()
        result = r.json()
    else:
        print r.text
    return result

def get_literature_breakdown(folderName, fileName):
    with open(folderName + fileName) as json_data:
        parkinsonLiteratureJson = json.load(json_data)

    json.dumps(parkinsonLiteratureJson)
    targets = {}  # Dictionary with target names for keys
    for evidence in parkinsonLiteratureJson['data']:
        targetName = evidence['target']['gene_info']['symbol']
        if targetName in targets:
            litRefs = targets[targetName]
            #print 'found ' + targetName
        else:
            targets[targetName] = {};  # Under each target key we will keep pieces of literature that are relevant

        litRefs = targets[targetName]  # this is dictionary with lit_id as key for each paper
        # stringOfLitRefs = targets[targetName]
        litRefList = evidence['literature']['references']  # the list of references
        for litRef in litRefList:
            url = litRef['lit_id']
            lit_id = litRef['lit_id'].split("/")[-1]
            litRefs[lit_id] = ""  # prepopulate with empty data

    #print targets

    for targetName in targets:
        #print "TargetName =" + targetName
        litDictionary = targets[targetName]
        absrtactIds = litDictionary.keys()
        query = " OR ".join("EXT_ID:" + item for item in absrtactIds)
        r = get_abstracts(query, targetName, folderName + targetName + ".json")
        resultList = r['resultList']['result']
        if resultList is not None:
            if len(resultList) > 0:
                for publication in resultList:
                    #print publication
                    paper_id = publication['pmid']
                    #print "paper_id = " + paper_id
                    litDictionary[paper_id] = publication
        #print targets

    #print targets
    return targets

def format_json_for_visualization(targets, fileName):
    articleList = []
    startYear = 2016
    endYear = 2016

    targetNames = targets.keys()
    for targetName in targetNames:
        targetDict = {}
        targetDict["name"] = targetName
        publications = targets[targetName]
        articlesYearList = [];  # this will look like this  [[2011, 2], [2013, 3]]
        articleYears = []
        total = 0
        # Publication years for each target
        for publicationId in publications.keys():
            publication = publications[publicationId]
            if type(publication) is dict:
                pubYear = int(publication['pubYear'])
                articleYears.append(pubYear)
        articleYearsSorted = sorted(articleYears)
        total = len(articleYears)
        c = Counter(articleYears)
        counterSorted = sorted(c.items(), key=itemgetter(0))
        articlesYearList = [list(theTuple) for theTuple in counterSorted]
        if startYear > articleYearsSorted[0]:
            startYear = articleYearsSorted[0]
        if endYear < articleYearsSorted[-1]:
            endYear = articleYearsSorted[-1]
        targetDict["articles"] = articlesYearList
        targetDict["total"] = total
        articleList.append(targetDict)

    json_article_list_string = json.dumps(articleList)
    json_article_list = json.loads(json_article_list_string)
    with open(fileName, 'w') as outfile:
        json.dump(json_article_list, outfile)
    #print startYear
    #print endYear

    return [startYear, endYear]

