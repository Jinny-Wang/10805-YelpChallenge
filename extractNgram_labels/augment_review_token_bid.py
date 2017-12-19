### Yelp Challenge
### December 16th 2017
### Jingyu Wang

## extract_review_token_withbid.py
## extract tokenized reviews with bid

import json
import csv
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
import mysql.connector
from mysql.connector import errorcode
import datetime
import numpy as np
def main():
    review_token = open("review_token_bid.csv",'r')
    review_token_augmented = open("review_token_augmented.csv",'w')
    rid_bid = np.load("revieid_bid.npy")
    writer = csv.writer(review_token_augmented,delimiter="\t",lineterminator="\n")
    reader = csv.reader(review_token,delimiter="\t")
    #review = open("/Users/jinny/Desktop/yelp challenge/data/dataset/review.json",'r')
    i = 0
    for row in reader:
        if i % 1000 == 0:
            print i
        rid = rid_bid[i][0]
        bid = rid_bid[i][1]
        if(rid != row[0]):
            print("reviews order doesn't match!")
            break
        review_text = row[2]
        store = [rid,bid,review_text]
        writer.writerow(store)
        i+=1
if __name__ == '__main__':
    #cnx = connect()
    main()
