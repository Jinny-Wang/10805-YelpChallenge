## 10-805 Machine Learning with Large Dataset  Final Project
## Yelp Challenge
## readDict.py
## Run after ngram.py
## Process the ngramDict generated.  Have a look at the top-K frequent 1gram,2gram,3gram,4gram
## Then set proper cutOff to generate ngramDictShrinked.json
## Date : Nov. 10th  2017
## Name : Jingyu Wang

## Assumption : Please install mysql connector on your macs

import json
import heapq
import matplotlib.pyplot as plt
def findNMaxinDict(d,N):
    res = [(0,'dummy') for i in range(N)]
    heapq.heapify(res)
    mn = 0
    for k in d:
        if d[k] > mn:
            heapq.heapreplace(res, (d[k],k))
            mn,key_mn = heapq.heappop(res)
            heapq.heappush(res,(mn,key_mn))
    return res

def shrinkDict(cutOff,d):
    for key,value in d.items():
        if value < cutOff:
            del d[key]

if __name__ == '__main__':

    with open('/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/rawNgram/ngramDict.json','r') as json_data:
        ngramDict = json.load(json_data)
        for i in range(len(ngramDict)):
            # res = findNMaxinDict(ngramDict[i],100)
            # res.sort(reverse=True)
            # print res
            # freq = [ngramDict[i][k] for k in ngramDict[i]]
            # freq.sort(reverse = True)
            # thres =  0.5
            # tmp = freq[0:int(len(freq)*thres)]
            # print i
            # print "len of freq: ",len(freq)
            # print "len of tmp: ",len(tmp)
            # print "cut off freq",tmp[len(tmp)-1]
            cutOff = [1000,3000,2000,1000] ## cutOff for 1-gram, 2-gram,3-gram, 4-gram respectively

            shrinkDict(cutOff[i],ngramDict[i])
            print i+1,len(ngramDict[i])
    with open('ngramDictShrinkedLevel2.json','w') as fp:
        json.dump(ngramDict, fp)
