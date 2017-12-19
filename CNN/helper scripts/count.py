import json
import csv

rawLabels = open("/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/CNN/labels.csv",'r')
LabelsReader = csv.reader(rawLabels,delimiter = '\t')

zero = 0
one = 0
two = 0
for row in LabelsReader:
    print row[2]
    if(int(row[2])==0):
        zero += 1
    elif(int(row[2])==1):
        one +=1
    elif(int(row[2])==2):
        two+=1
    else:
        print "Something Wrong!"
        print row
        print row[2]
        break

print zero,one,two
