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
import datetime
import numpy as np
def main():

    review = open("/Users/jinny/Desktop/yelp challenge/data/dataset/review.json",'r')
    outfile = open("revieid_bid.npy",'w')
    count = 0
    res = []
    for row in review:
        count += 1
        if count % 1000 == 0:
            print count
        row = json.loads(row)
        review_id = row['review_id']
        bid = row['business_id']
        res.append([review_id,bid])
    res = np.array(res)
    np.save(outfile,res)
if __name__ == '__main__':
    #cnx = connect()
    main()
