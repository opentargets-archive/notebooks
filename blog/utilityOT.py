import requests
import json
import urllib
import gzip
import os.path
import random


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
    result = r.json()
    if result["data"][0]["data"]["approved_symbol"] == genesymbol:
         geneId = result["data"][0]["id"]
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
    #Below is just a sample baseline api call to test that api is working
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
        print theLine
        #take second column
        theColumns = theLine.split("\t", 2)
        if len(theColumns) >=2:
            secondColumn =  theColumns[1]
        
            if secondColumn.endswith('withdrawn') == False:
                print secondColumn
                writeTo.write(secondColumn + "\n")
    
    readFrom.close()
    writeTo.close()
    return None

def get_random_gene_names(filename='hgnc_symbol_set.txt', numGenes=10):
    #load all the lines in file into genes list, but strip newline/whitespace first
    with open('hgnc_symbol_set.txt') as f:
        genes = [line.rstrip() for line in f]
    random.shuffle(genes)
    print(genes[:numGenes])
    random_genes = [utilityOT.get_ensid(x) for x in genes[:numGenes] if get_ensid(x) is not None]
    print random_genes
    return ramdom_genes

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
def get_ens_genes(geneNames):
    ens_genes = [get_ensid(x) for x in geneNames if get_ensid(x) is not None]    
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
    
    diseaseResults = open(disease + '_targets_'+ fileName+ '.csv','w')
    diseaseResults.write(r.text)
    diseaseResults.close()
    
    return r.text
#def save_to_file_with_requests():   
#     with open('output.jpg', 'wb') as handle:
#        response = requests.get('http://www.example.com/image.jpg', stream=True)
#    
#        if not response.ok:
#            # Something went wrong
#    
#        for block in response.iter_content(1024):
#            handle.write(block)   
    
