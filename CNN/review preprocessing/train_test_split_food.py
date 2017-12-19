## 10805- Yelp Challenge
## train test split
## randomly shuffle review text
## and divide them into train vs test

## store  clustername_train.txt  clustername_test.txt

import csv
import sys
import json
import random
import numpy as np
import math

clustername = ['Active Life','Arts & Entertainment','Automotive','Beauty & Spas','Education',
                'Event Planning & Services','Fashion','Financial Services','Food','Grocery',
                'Health & Medical','Home & Garden','Home Services','Hotels & Travel','Nightlife',
                'Pets','Real Estate','Shopping']

clustered_review_path = "/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/clustered_reviews/"

# format : [[rid,bid,score,valid]]
labels = np.load("/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/labels/labels_full_validated.npy")
reader = csv.reader(labels,delimiter = '\t')

## cluster: string name  e.g. "Food"
def train_test_split(cluster,seed,test_percentage):
    i = 0
    review_filename = clustered_review_path+ cluster  + ".txt"
    # r_id = []
    # r_text = []
    # r_labels = []
    reviews = []
    review = open(review_filename,'r')
    for line in review:
        if i % 1000 == 0:
            print cluster,i
        line = line.split('\t')
        rid = line[0]
        rtext = line[1]
        while(labels[i][0] != rid):
            i+=1
        if int(labels[i][3]) != 1:
            continue
        label_i = 1 if int(labels[i][2]) > 0 else 0
        reviews.append([rid,rtext,label_i])

    reviews = np.array(reviews)
    # np.random.seed(seed)
    # shuffle_indices = np.random.permutation(np.arange(len(reviews)))
    # print ('shuffling reviews')
    # splitted = np.array_split(reviews, len(reviews)//6, axis=0)
    # for i  in range(len(splitted)):
    #     shuffle_indices = np.random.permutation(np.arange(len(splitted[i])))
    #     reviews_shuffled = splitted[i][shuffle_indices]
    #     if i == 0 :
    #         reviews_shuffled_total = reviews_shuffled
    #     else:
    #         reviews_shuffled_total = np.concatenate((reviews_shuffled_total,reviews_shuffled),axis=0)
    #
    # #reviews_shuffled = reviews[shuffle_indices]
    # print ('finish shuffling')

    print ('train test split')
    dev_sample_index = -1 * int(test_percentage * float(len(reviews)))
    reviews_train, reviews_test = reviews[:dev_sample_index], reviews[dev_sample_index:]
    print ('finish train test split')

    outfile1 = open("/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/clustered_reviews_shuffled/"+cluster+"/train_id.npy",'w')
    outfile2 = open("/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/clustered_reviews_shuffled/"+cluster+"/test_id.npy",'w')
    # outfile3 = open("/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/clustered_reviews_shuffled/"+cluster+"/train_all.npy",'w')
    # outfile4 = open("/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/clustered_reviews_shuffled/"+cluster+"/test_all.npy",'w')
    print ('begin saving')
    np.save(outfile1,reviews_train[:,0]) #train id
    np.save(outfile2,reviews_test[:,0]) # test id
    # np.save(outfile3,reviews_train)
    # np.save(outfile4,reviews_test)
    print('finish saving')
    with open("food_train.txt",'w') as fp:
        for i in range(len(reviews_train)):
            if i % 1000 == 0:
                print "train ",i
            fp.write(reviews_train[1])
            fp.write('\t')
            fp.write(reviews_train[2])
            fp.write('\n')

    with open("food_test.txt",'w') as fpt:
        for i in range(len(reviews_test)):
            if i % 1000 == 0:
                print "test ",i
            fpt.write(reviews_test[1])
            fpt.write('\t')
            fpt.write(reviews_test[2])
            fpt.write('\n')

seed = 10
test_percentage = 0.1
train_test_split('Food',seed,test_percentage)

# for cluster in clustername[15:]:
#     print("processing cluser" + cluster)
#     seed = 10
#     test_percentage = 0.1
#     train_test_split(cluster,seed,test_percentage)
