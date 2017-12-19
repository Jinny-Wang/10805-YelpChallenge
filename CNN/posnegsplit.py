##split useful and unuseful reviews, used for training CNN

import csv
import sys
import pandas as pd
import json
rawNgram = open("/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/rawNgram/1gram.csv",'r')
rawLabels = open("/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/CNN/labels_full.csv",'r')

# useful1 = open("useful1.pos",'w')
# useful2 = open("useful2.pos",'w')
notuseful = open("notuseful_full.neg",'w')
useful = open("useful_full.pos",'w')

# a = pd.read_csv("/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/CNN/1gramShrink.csv",delimiter = '\t')
# b = pd.read_csv("/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/CNN/labels.csv",delimiter = '\t')
# print a
# # merged = a.merge(b)
# # merged.to_csv("output.csv", index=False)
#

NgramReader = csv.reader(rawNgram,delimiter = '\t')
LabelsReader = csv.reader(rawLabels,delimiter = '\t')
labels = dict()
for row in LabelsReader:
    labels[row[0]] = int(row[1])

with open('labelsdict_full.json','w') as fp:
    json.dump(labels, fp)
    #labels = json.load(fp)

count = 0
for row in NgramReader:
    count+=1

    if count % 1000 == 0:
        print count
    if row[0] in labels:
        if labels[row[0]] > 0 :
            # useful.write(row[0]) ##id
            # useful.write('\t')
            useful.write(row[1])
            useful.write('\n')
        else:
            # notuseful.write(row[0]) ##id
            # notuseful.write('\t')
            notuseful.write(row[1])
            notuseful.write('\n')
        # if labels[row[0]]==1:
        #     useful1.write(row[1])
        #     useful1.write('\n')
        # elif labels[row[0]]==2:
        #     useful2.write(row[1])
        #     useful2.write('\n')
