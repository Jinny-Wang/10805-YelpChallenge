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

def main():
    outfile = open("review_token_bid.csv",'w')
    writer = csv.writer(outfile,delimiter="\t",lineterminator="\n")
    review = open("/Users/jinny/Desktop/yelp challenge/data/dataset/review.json",'r')
    # cursor = cnx.cursor()
    # query = ("SELECT id,business_id,text FROM review")
    #
    # cursor.execute(query) ## note !! pass  (state,) to create a tuple of strings!!
    # results = cursor.fetchall()
    count = 0
    lmtzr = WordNetLemmatizer()
    stop = set(stopwords.words('english'))
    for row in review:
        count += 1
        if count % 1000 == 0:
            print count
        row = json.loads(row)
        row_text = row['text']
        row_tokens = word_tokenize(row_text)
        #remove punctuation
        row_tokens = [l.lower() for l in row_tokens if l not in string.punctuation or l=="?" or l=="!"]

        #Lemmatization
        row_tokens = [lmtzr.lemmatize(c,"v") for c in row_tokens]

        #Remove stopwords
        row_tokens = [c.lower() for c in row_tokens if c not in stop]
        #All tokens will be space-separated
        text_store = " ".join(row_tokens).encode('utf-8').strip()
        #Write to csv
        store = [row['review_id'],row['user_id'],text_store]
        writer.writerow(store)

if __name__ == '__main__':
    #cnx = connect()
    main()
