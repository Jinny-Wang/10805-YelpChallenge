## 10-805 Machine Learning with Large Dataset  Final Project
## Yelp Challenge
## ngram.py
## Extract n-gram features from tokenized text.
## And store them back as a new column in the review_token table.

## Date : Nov. 10th  2017
## Name : Jingyu Wang

## Assumption : Please install mysql connector on your macs

import mysql.connector
from mysql.connector import errorcode
import datetime
import string
import csv
import json

## connect to the mysql server
def connect():
    # step 1 : connect to the remote MySQL server
    try:
      cnx = mysql.connector.connect(user='Admin10805', password='10805fall2017',
                                  host='yelp2.csfuygoxtob2.us-east-2.rds.amazonaws.com',
                                  database='yelp_db')
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    return cnx
    # else:
    #   cnx.close()

## extract 2, 3, 4 grams from the text
def extract(cnx,fileNameList):

    global N
    print("start to extract up to %d gram" % (N))
    # step 2 : query the data
    cursor = cnx.cursor()
    query = ("SELECT * FROM review_token")

    cursor.execute(query) ## note !! pass  (state,) to create a tuple of strings!!
    results = cursor.fetchall()

    fileList = [open(fileNameList[i],'w') for i in range(len(fileNameList))]
    csvWriterList = [csv.writer(fileList[i], delimiter='\t',lineterminator='\n') for i in range(len(fileList))]
    count_row = 0
    for row in results:
        count_row += 1
        if(count_row % 1000 == 0):
            print "processing review # ",count_row
            printDictSize()
        if(count_row % 10000 == 0):
            shrinkDict()
            printDictSize()

        text= row[1]
        text  = text.split()
        for i in range(1,N+1): # 1... N
            if(i==1):
                for token in text:
                    updateDict(1,token)
            else:
                ngramText = ngram(i,text)
                ngramStore = [row[0],ngramText]
                csvWriterList[i-2].writerow(ngramStore)

    for i in range(len(fileList)):
        fileList[i].close()
    print ("extracting ngram ends")

## ngram:
## given a list of one gram tokens
## return the space sperated n-gram , n passed as argument
## example : given text  =  ['like','macdonald','haha','food']
## n = 2
## return :  "like+macdonald macdonald+haha haha+food"
def ngram(n,text):
    res = []
    for i in range(len(text)-n+1):
        tmp = text[i:i+n]
        tmp = '+'.join(tmp)
        res.append(tmp)
        updateDict(n,tmp)
    return ' '.join(res).encode('utf-8').strip()


## remove item whose occurence is less than
## 2 time
def shrinkDict():
    global ngramDict
    for i in range(len(ngramDict)):
        for key,value in ngramDict[i].items():
            if value <=2 :
                del ngramDict[i][key]


def printDictSize():
    global ngramDict
    for i in range(len(ngramDict)):
        size = len(ngramDict[i])
        print "size for "+str(i+1)+"gram dict : ", size

## updateDict
## update the global ngramDict
## increase the count of corresponding ngram combination by 1
def updateDict(n,ngramText):
    global ngramDict
    if (ngramText in ngramDict[n-1]):
        ngramDict[n-1][ngramText] += 1
    else:
        ngramDict[n-1][ngramText] = 1

if __name__ == '__main__':
    global N
    N= 4 # extract 1, 2, 3, 4 gram
    global ngramDict
    ngramDict= [ dict() for i in range(N)]
    cnx = connect()
    fileNamePrefix = "gram"
    fileNameList = [ str(i+1)+fileNamePrefix+".csv" for i in range(1,N)]
    print fileNameList
    extract(cnx,fileNameList)

    for i in range(N):
        print len(ngramDict[i])
    with open('ngramDict.json', 'w') as fp:
        json.dump(ngramDict, fp)
