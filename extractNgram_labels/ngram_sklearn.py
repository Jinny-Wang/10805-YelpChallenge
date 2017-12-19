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
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

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
def extract(cnx):
    global N
    print("start to extract up to %d gram" % (N))
    # step 2 : query the data
    cursor = cnx.cursor()
    query = ("SELECT text FROM review_token LIMIT 10000")

    cursor.execute(query) ## note !! pass  (state,) to create a tuple of strings!!
    result = cursor.fetchall()
    corpus = [row[0] for row in result]
    #print corpus
    vectorizer = CountVectorizer(input='content', encoding='utf-8', decode_error='strict', strip_accents=None, lowercase=False,
    preprocessor=None, tokenizer=None, stop_words=None,
    token_pattern='(?u)\\b\\w\\w+\\b',
    ngram_range=(1, 4), analyzer='word',
    max_df=1.0, min_df=3, max_features=None, vocabulary=None, binary=False, dtype=np.int64)
    X = vectorizer.fit_transform(corpus)
    store = X.toarray()
    ngramDict = vectorizer.vocabulary_
    return store,ngramDict
if __name__ == '__main__':
    global N
    N= 4 # extract 1, 2, 3, 4 gram
    # global ngramDict
    # ngramDict= [ dict() for i in range(N)]
    cnx = connect()
    store ,ngramDict = extract(cnx)
    print len(ngramDict)
    print store.shape
    with open("sklearn-ngram.csv",'w') as f:
        writer = csv.writer(f, delimiter='\t',lineterminator='\n')
        for row in store:
            writer.writerow(row)
            
    with open('ngramDict.json', 'w') as fp:
        json.dump(ngramDict, fp)
