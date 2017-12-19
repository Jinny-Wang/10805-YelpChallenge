import mysql.connector
from mysql.connector import errorcode
import datetime
import string
import csv
import json
from operator import itemgetter
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
def sampleIndex():
    res = []
    with open('sample.csv','r') as f:
        reader = csv.reader(f,delimiter=',')
        isFirst = True
        for row in reader:
            if(isFirst):
                isFirst = False
                continue
            if(len(row) < 2):
                continue
            try:
                res.append((row[0],int(row[1])))
            except:
                print row
    res.sort(key=itemgetter(1))
    return res

def scoretoCat(score):
    if(score ==0):
        return 0 #not useful
    elif(score <= 7):
        return 1 #neutral
    else:
        return 2 #useful

def extractLabels(cnx):
    cursor = cnx.cursor()
    query = ("SELECT id,useful+funny+cool FROM review")

    cursor.execute(query) ## note !! pass  (state,) to create a tuple of strings!!
    results = cursor.fetchall()
    labelsFile = open('labels.csv','wb')
    writer = csv.writer(labelsFile,delimiter='\t',lineterminator='\n')
    sampleWriter = csv.writer(open('sample_new.csv','wb'),delimiter='\t',lineterminator='\n')
    sample  = sampleIndex()
    sampleset = set([sample[i][0] for i in range(len(sample))])
    rowIndex = 0
    for row in results:
        rowIndex += 1
        if rowIndex % 1000 == 0:
            print rowIndex

        reviewID = row[0]
        score = row[1]
        #print reviewID, score , sample[sampleCount][0]
        if reviewID in sampleset:#rowIndex == sample[sampleCount][1] and reviewID == sample[sampleCount][0]:
            cat = scoretoCat(score)
            sampleWriter.writerow([reviewID,rowIndex])
            writer.writerow([reviewID,rowIndex,cat])
if __name__ == '__main__':
    cnx = connect()
    extractLabels(cnx)
