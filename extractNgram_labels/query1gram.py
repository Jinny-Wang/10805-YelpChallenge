## extract 1gram from review_token table
## store it as 1gram.csv
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
def extractOneGram(cnx):
    cursor = cnx.cursor()
    query = ("SELECT * FROM review_token")

    cursor.execute(query) ## note !! pass  (state,) to create a tuple of strings!!
    results = cursor.fetchall()
    onegramFile = open('1gram.csv','wb')
    writer = csv.writer(onegramFile,delimiter='\t',lineterminator='\n')
    count = 0
    for row in results:
        count += 1
        if count % 1000 == 0:
            print count
        text = row[1]
        text= text.split()
        text = ' '.join(text).encode('utf-8').strip()
        writer.writerow([row[0],text])

if __name__ == '__main__':
    cnx = connect()
    extractOneGram(cnx)
