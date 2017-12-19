## 10-805 Machine Learning with Large Dataset  Final Project
## Yelp Challenge
## vectorization.py
## vectorized the n-gram features using bag-of-words representation
## And store them back as a new column in the review_token table.

## Date : Nov. 12nd  2017
## Name : Jingyu Wang
## Stay alive!

import json
import csv
import numpy as np


## convert ngramdict to
## key:Index
## index corresponds to index in the feature vector
def readDict(filename,featureToIndex):
    res = []
    with open(filename,'r') as json_data:
        ngramDict = json.load(json_data)
        for i in range(len(ngramDict)):
            print "processing dict", i
            count = 0
            for k in ngramDict[i]:
                ngramDict[i][k] = count
                count += 1
            res.append(ngramDict[i])
        with open(featureToIndex,'wb') as fp:
            json.dump(res,fp)
    return res


def sampleVec(samplefilename):
    res = []
    with open(samplefilename,'r') as sample:
        reader = csv.reader(sample,delimiter='\t')
        for row in reader:
            res.append(int(row[1]))
    return res


## BOW vectorization
def vectorize(size,feature, ngramText):
    res = np.zeros(size)
    for item in ngramText:
        if item in feature:
            res[feature[item]] = 1
    return res

def ngramTexttoVec(ngramFileName,features,ngramBOWFileName,sample):
    for i in range(len(ngramFileName)):
        featureSize = len(features[i+1])
        #res = []
        with open(ngramFileName[i],'r') as ngram:
            reader = csv.reader(ngram,delimiter='\t')
            with open(ngramBOWFileName[i],'wb') as outfile:
                writer = csv.writer(outfile,delimiter='\t',lineterminator='\n')
                count = 0
                sampleIndex = 0
                for row in reader:
                    count +=1
                    if count % 1000 == 0 :
                        print str(2)+'gram:' , count
                    if count == sample[sampleIndex]:
                        ngramText = row[1].split()
                        v = vectorize(featureSize,features[i+1],ngramText)
                        writer.writerow(v)
                        sampleIndex += 1





if __name__ == '__main__':
    ngramDictFileName = '/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/baselineTrail/shrinkLevel2/ngramDictShrinkedLevel2.json'
    samplefilename = '/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/baselineTrail/sample_new.csv'
    featureToIndex = '/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/baselineTrail/featureToIndex.json'

    ## Get feature to Index dictionary
    features = readDict(ngramDictFileName,featureToIndex)

    ## readin sample
    sample = sampleVec(samplefilename)

    shrinkedNgramPrefix = '/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/baselineTrail/'
    N = 3
    ngramFileName = [shrinkedNgramPrefix+str(i)+'gramShrinkLevel2.csv' for i in range(2,N)]
    ngramBOWFileName = [shrinkedNgramPrefix+str(i)+'gram-BOW.csv' for i in range(2,N)]

    ngramTexttoVec(ngramFileName,features,ngramBOWFileName,sample)
