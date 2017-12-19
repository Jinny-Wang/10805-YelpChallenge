## extract usefulness labels from ALL the reviews
## add validity labels : only reviews before 2016-1-1 is valid
## usefulness = useful + funny + cool
## Date : December 17th 2017
## store in labels_full_validated.csv
## Format : reviewid, businessid, score, validity
## reviews are laoded from local json


import json
from datetime import datetime
import string
import csv
import json
import numpy

def extractValidLabels():
    review = open("/Users/jinny/Desktop/yelp challenge/data/dataset/review.json",'r')
    outfile = open("labels_full_validated.csv",'w')
    writer = csv.writer(outfile,delimiter = '\t',lineterminator='\n')
    date_format = "%Y-%m-%d"
    first = datetime.strptime('2004-07-22',date_format)

    count = 0
    for row in review:
        count += 1
        if count % 1000 == 0:
            print count
        row = json.loads(row)
        review_id = row['review_id']
        buz_id = row['business_id']
        score = int(row['useful'])+int(row['funny'])+int(row['cool'])
        day_diff = datetime.strptime(row['date'], date_format) - first
        day_diff = day_diff.days
        isValid = 1 if day_diff < 4180 else 0
        towrite = [review_id, buz_id, score ,isValid]
        writer.writerow(towrite)

if __name__ == '__main__':
    extractValidLabels()
