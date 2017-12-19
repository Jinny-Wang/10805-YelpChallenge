
## 10-805 Machine Learning with Large Dataset  Final Project
## Yelp Challenge
## ngram.py
## Extract n-gram features from tokenized text.
## And store them back as a new column in the review_token table.

## Date : Nov. 10th  2017
## Name : Jingyu Wang

import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

import random
from random import randint
import time
import scipy
import csv
import json


def getAccuracy(y, predictions):
    correct = 0
    for x in range(len(y)):
        if y[x] == predictions[x]:
            correct += 1
    return (correct/float(len(y))) * 100.0


def readInfeature(filename,sub_sample):
    res = []
    sub_sample_size = len(sub_sample)
    with open(filename,'r') as infile:
        reader = csv.reader(infile,delimiter = '\t')
        i = 0 # count for row_index
        j = 0 # count for sub_sampling
        for row in reader:
            i+= 1
            #print "processing feature row ",i
            if(i == sub_sample[j]):
                row  = map(float,row)
                print "appended row",sub_sample[j]
                res.append(row)
                j+=1
                if(j >= sub_sample_size):
                    break
    return res

def readInLabels(filename,sub_sample):
    res = []
    sub_sample_size = len(sub_sample)
    with open(filename,'r') as infile:
        reader = csv.reader(infile,delimiter = '\t')
        i = 0 # count for row_index
        j = 0 # count for sub_sampling
        for row in reader:
            i+= 1
            #print "processing labels row ",i
            if(i == sub_sample[j]):# 0: not useful , 1 : neutral , 2: highly useful
                category = row[2]
                print "appended labels",sub_sample[j]
                res.append(category)
                j+=1
                if(j >= sub_sample_size):
                    break
    return res


def baseLine(X_train, X_test, y_train, y_test ):
    ## use the svm
    print('Train the SVM classifier')
    """ your code here """
    svm_model=svm.SVC(kernel='rbf')#kernel='rbf' by default
    svm_model=svm_model.fit(X_train,y_train)
    print('Finish Train the SVM classifier')
    svm_train_pred=svm_model.predict(X_train)
    svm_test_pred = svm_model.predict(X_test)
    print('Finish Predicting')

    train_f1 = f1_score(y_train,svm_train_pred,average=None)
    test_f1 = f1_score(y_test,svm_test_pred,average=None)
    train_accuracy = accuracy_score(y_train,svm_train_pred)
    test_accuracy = accuracy_score(y_test,svm_test_pred)
    train_recall = recall_score(y_train,svm_train_pred,average=None)
    test_recall = recall_score(y_test,svm_test_pred,average=None)
    train_precision = precision_score(y_train,svm_train_pred,average=None)
    test_precision = precision_score(y_test,svm_test_pred,average=None)


    print ("The evaluation of sk-learn implemented SVM")
    print ("accuracy : train %f, test %f "%(train_accuracy,test_accuracy))

    print ("f1 socre : train ")
    print train_f1
    print ("f1 score : test")
    print test_f1

    print ("recall : train ")
    print train_recall
    print ("recall : test")
    print test_recall

    print ("precisoin : train ")
    print train_recall
    print ("precision: test")
    print test_recall
    return svm_train_pred,svm_test_pred
    # svm_model = ...

    # ## use the random forest
    # print('Train the random forest classifier')
    # """ your code here """
    # rf_model = RandomForestClassifier(random_state=3)#n_estimators=10 by default number of trees in the forest.
    # rf_model = rf_model.fit(X_train,y_train)
    # rf_pred=rf_model.predict(X_train)
    # acc4=getAccuracy(y_train, rf_pred)
    # print ("The accuracy of sk-learn implemented SVM : %f" %(acc4))
    # print("\n")
    # # rf_model = ...

if __name__ == '__main__':
    random.seed(0)

    sub_sample =  random.sample(range(1, 303400), 50000)
    sub_sample.sort()

    filename = "/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/baselineTrail/vectorizedBOW/1gram-BOW.csv"
    labelsFilename = '/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/baselineTrail/labels.csv'
    X = readInfeature(filename,sub_sample)
    y = readInLabels(labelsFilename,sub_sample)
    # X = [[1,2,3],[4,5,6],[4,5,6],[4,5,6],[4,5,6],[4,54,6],[4,5,6],[43,5,6],[4,5,16],[4,5,36]]
    # y = [1,0,1,2,1,0,0,1,5,8]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    train_pred,test_pred = baseLine(X_train, X_test, y_train, y_test )
    outfile1 = open('y_train.npy','w')
    outfile2 = open('y_test.npy','w')
    outfile3 = open('train_pred.npy','w')
    outfile4 = open('test_pred.npy','w')
    np.save(outfile1,y_train)
    np.save(outfile2,y_test)
    np.save(outfile3,train_pred)
    np.save(outfile4,test_pred)
