import numpy as np
import sys
import csv
import json

rawNgram = open("/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/CNN/1gramShrinkLevel2.csv",'r')
rawLabels = open("./labels_validated_updated.csv",'r')
predictions = open('./prediction_prob.csv','r')
prediction_idx = open('./prediction_idx_CNN.csv','w')
prediction_prob  = np.load('./cnn_pred_score.npy')
NgramReader = csv.reader(rawNgram,delimiter = '\t')
predictionReader = csv.reader(predictions,delimiter = ',')
# newpredwriter = csv.writer(prediction_idx,delimiter=',')

def softMax(x):
    mx = np.max(x,axis=1).reshape(x.shape[0],1)
    shift = x - mx
    exps = np.exp(shift)
    deno = np.sum(exps,axis=1).reshape(exps.shape[0],1)
    return exps/deno

prediction_prob = softMax(prediction_prob)
print (prediction_prob)
LabelsReader = csv.reader(rawLabels,delimiter = '\t')
labels = dict()
for row in LabelsReader:
    if(int(row[3])==1):
        labels[row[0]] = int(row[2])
x_pos = []
x_neg = []

count = 0
reviews = dict()

for row in NgramReader:
    count+=1
    if count % 1000 == 0:
        print (count)
    if row[0] in labels:
        reviews[row[1]] =  row[0]        #key : text, value: reviewid

i = 0
res = []
prob = []
for row in predictionReader:
    reviewid = reviews[row[0]]
    # newpredwriter.writerow([reviewid,row[0],row[1]])
    res.append([reviewid,float(row[1])])
    print (prediction_prob[i])
    prob.append([reviewid,prediction_prob[i][1],prediction_prob[i][0]]) # id , positivelabel prob, negative label prob
    i += 1
    if(i % 1000 ==0):
        print ("row ",i)
outfile = open("cnnprediction_prob.npy",'wb')
np.save(outfile,np.array(prob))
