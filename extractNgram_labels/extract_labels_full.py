## extract usefulness labels from ALL the reviews
## usefulness = useful + funny + cool
## Date : December 16th 2017
## store in labels_full.csv
## format : review_id, useful+funny+cool
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
def extractLabels(cnx):
    cursor = cnx.cursor()
    query = ("SELECT id, useful+funny+cool FROM review")

    cursor.execute(query) ## note !! pass  (state,) to create a tuple of strings!!
    results = cursor.fetchall()
    labelsFile = open('labels_full.csv','wb')
    writer = csv.writer(labelsFile,delimiter='\t',lineterminator='\n')
    count = 0
    for row in results:
        count += 1
        if count % 1000 == 0:
            print count
        writer.writerow([row[0],row[1]])

if __name__ == '__main__':
    cnx = connect()
    extractLabels(cnx)
