from pybliometrics.scopus import ScopusSearch
from datetime import datetime
import collections
import pandas as pd
import os

class Query:
    def __init__(self, fileName, groupsOR, subjectAreas, operatorYear, yearEqualTo, groupNot, preQueryForTitles):
        self.fileName=fileName
        self.groupsOR=groupsOR
        self.subjectAreas=subjectAreas
        self.operatorYear=operatorYear
        self.yearEqualTo=yearEqualTo
        self.groupNot=groupNot
        self.preQueryForTitles=preQueryForTitles
        

def getPapers(query):  
    s=ScopusSearch(getQueryString(query), verbose=True, subscriber=False) 
    df = pd.DataFrame(pd.DataFrame(s.results))
    if (s.get_results_size()>0):
        pd.set_option('display.max_columns', None)
        if (query.operatorYear=="<"):
            nombreOp="lT"
        if (query.operatorYear==">"):
            nombreOp="mT"
        if (query.operatorYear=="="):
            nombreOp="eT"
        query.fileName = query.fileName + '-' + nombreOp + str(query.yearEqualTo) + '-res' + str(s.get_results_size()) 
        query.fileName = query.fileName + '-date'+ datetime.now().strftime("%d.%m.%y-%H.%M") 
        
        if not os.path.exists('Queries'):
            os.makedirs('Queries')
        df.to_csv('Queries/' + query.fileName + ".csv")
    else:
        print('No results for year ' + str(query.yearEqualTo))

def getQueryString(query): 
    queryString=query.preQueryForTitles  
    if  len(query.groupsOR) == 0:
        return 'Nothing to compare'      
    if query.groupsOR.count == 1:
        queryString='(' + concatORTitleAbsKey(list(set(query.groupsOR[0]))) + ')'
    else: 
        queryString=queryString +'('       
        for group in query.groupsOR:
            queryString=queryString + concatORTitleAbsKey(list(set(group))) + ') AND ('
        queryString  = queryString[:-5]
    
    if  len(query.subjectAreas) > 0:
        queryString=queryString + ' AND ('
        queryString=queryString  + concatORSubjectAreas(list(set(query.subjectAreas)))       
        queryString=queryString + ')'
    
    if (query.yearEqualTo=="" or query.operatorYear==""):
        queryString=queryString + ' AND PUBYEAR > ' + ' 1 ' + ' '
    else:     
        if (query.operatorYear==">"):    
            queryString=queryString + ' AND PUBYEAR > ' + str(query.yearEqualTo) + ' '
        
        if (query.operatorYear=="<"):
            queryString=queryString + ' AND PUBYEAR < ' + str(query.yearEqualTo) + ' '
        
        if (query.operatorYear=="="):
            queryString=queryString + ' AND PUBYEAR = ' + str(query.yearEqualTo) + ' '

    if  len(query.groupNot) > 0:
        queryString = queryString + 'AND NOT ('+ concatORTitleAbsKey(query.groupNot)  + ')'
   
    return queryString

def concatORTitleAbsKey(termList): 
    combinationOr ='TITLE-ABS-KEY("'+ termList[0] + '")'
    for x in termList[1:]:       
        combinationOr += ' OR TITLE-ABS-KEY("'+ x +'")' 
    return combinationOr

def concatORTitle(termList): 
    combinationOr ='TITLE("'+ termList[0]  + '")'
    for x in termList[1:]:       
        combinationOr += ' OR TITLE("'+ x +'")'   
    return combinationOr  

def concatORSubjectAreas(subjectAreas): 
    combinationOr ='SUBJAREA('+ subjectAreas[0] + ')'
    for x in subjectAreas[1:]:       
        combinationOr += ' OR SUBJAREA('+ x +')'   
    return combinationOr  

def printFrequentWordsKeywords(CSVfilename, occurrencesGreaterThan):
    df = pd.read_csv('Queries/' + CSVfilename + '.csv', usecols= ['authkeywords'])
 
    string = ' '.join(map(str, df.values.tolist()))

    specialCharacters = "[]“””‘,\/?(−)'-:!.&;=" 
    for specialCharacters in specialCharacters:
        string = string.replace(specialCharacters, ' ')

    string = string.replace('"', " ")
    string=string.lower()

    words = string.split()
    word_counts = collections.Counter(words)

    string = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))
 
    dictionary=collections.OrderedDict(string)

    #In order to see all the words, you may have to update VSCode scrolling preferences. 
    for key in dictionary:
        if (dictionary[key] > occurrencesGreaterThan):
            print(key, ': ', dictionary[key])

def printFrequentWordsTitleAbsKey(CSVFilename, occurrencesGreaterThan):
    df = pd.read_csv('Queries/' + CSVFilename + '.csv', usecols= ['title', 'description','authkeywords'])
 
    string = ' '.join(map(str, df.values.tolist()))

    specialCharacters = "[]“””‘,\/?(−)'-:!.&;=" 
    for specialCharacters in specialCharacters:
        string = string.replace(specialCharacters, ' ')

    string = string.replace('"', " ")
    string=string.lower()

    words = string.split()
    word_counts = collections.Counter(words)

    string = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))
 
    dictrionary=collections.OrderedDict(string)

    #In order to see all the words, you may have to update VSCode scrolling preferences. 
    for key in dictrionary:
        if (dictrionary[key] > occurrencesGreaterThan):
            print(key, ': ', dictrionary[key])

def printFrequentWordsTitle(CSVFilename, occurrencesGreaterThan):
    df = pd.read_csv('Queries/' + CSVFilename + '.csv', usecols= ['title'])
 
    string = ' '.join(map(str, df.values.tolist()))

    specialCharacters = "[]“””‘,\/?(−)'-:!.&;=" 
    for specialCharacters in specialCharacters:
        string = string.replace(specialCharacters, ' ')

    string = string.replace('"', " ")
    string=string.lower()

    words = string.split()
    word_counts = collections.Counter(words)

    string = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))
 
    dictionary=collections.OrderedDict(string)

    #In order to see all the words, you may have to update VSCode scrolling preferences. 
    for key in dictionary:
        if (dictionary[key] > occurrencesGreaterThan):
            print(key, ': ', dictionary[key])

def printDOIs(CSVFilename):  
    df= pd.read_csv('Queries/' + CSVFilename + '.csv', usecols= ['doi'])    
    string = ' '.join(map(str, df.values.tolist()))   
    string = string.replace('[nan]', '')
    string = string.replace(']', ',')
    string = string.replace('[', '')
    string = string.replace("'", '')

    if (len(df) > 1):
        string = string[:-1]
    
    print(string)

def mergeCSVSFromFolder(folder_path):
    csv_list = []
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            csv_list.append(df)
    combined_csv = pd.concat(csv_list, ignore_index=True)
    combined_csv.to_csv('Queries/queriesCombined.csv', index=False)
