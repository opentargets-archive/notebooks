'''
    I have a disease and target and I want to see the evidence and break it down
    
    1)Show the weight of genetic evidence behind the link (divide in mendelian vs gwas)
    2)displays list of top 3 diseases, name and Association Score.
    3)show number of disease associations
    4)show pathway and .groupby pathway so that you bring the genes with shared biology at the top
'''

#Lets start with simple case - such as one target and one disease at first

PARKINSON_EFO = utilityOT.get_efoid('parkinson')
ATP13A2 = utilityOT.get_efoid('ATP13A2')
SNC     = utilityOT.get_efoid('SNC')

'''api/latest/public/association/filter - this API will give you just a summary
   of evidece for association - the numbers for each type of evidence
   So it is a starting point if you need to see several .
   
   Question - does association api accept several targets and several diseases??
'''

'''
    So for more info for evidence should use 
    https://www.targetvalidation.org/api/latest/public/evidence/filter?target=ENSG00000167207&disease=EFO_0003767&datatype=genetic_association&datastructure=full

http https://www.targetvalidation.org/api/latest/public/evidence/filter target==ENSG00000167207 disease==EFO_0003767 datastructure==simple size==10000 datatype==genetic_association >>  EBD_NOD2_evidence_genetic_simple_10000.json 
http https://www.targetvalidation.org/api/latest/public/evidence/filter target==ENSG00000167207 disease==EFO_0003767 datastructure==simple datatype==genetic_association >>  EBD_NOD2_evidence_genetic_simple_10.json 
http https://www.targetvalidation.org/api/latest/public/evidence/filter target==ENSG00000167207 disease==EFO_0003767 datastructure==full datatype==genetic_association >>  EBD_NOD2_evidence_genetic_full_10.json 
http https://www.targetvalidation.org/api/latest/public/evidence/filter target==ENSG00000167207 disease==EFO_0003767 datastructure==full size==10000 datatype==genetic_association >>  EBD_NOD2_evidence_genetic_full_10000.json
'''

