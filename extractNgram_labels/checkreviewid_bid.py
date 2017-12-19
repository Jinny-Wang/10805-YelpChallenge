import json
import csv
import numpy as np

reader = csv.reader(open("review_token_augmented.csv",'r'),delimiter = '\t')

rid_bid = np.load("revieid_bid.npy")
R2B_yi = json.load(open("R2B.json",'r'))

for i in range(len(rid_bid)):
    if i % 1000 == 0:
        print i
    rid_me = rid_bid[i][0]
    bid_me = rid_bid[i][1]

    if rid_me not in R2B_yi:
        print ("my reviews contain something more!!")
        break
    bid_yi = R2B_yi[rid_me]
    if bid_yi != bid_me :
        print ("business id doesn't match for the same review!")
        print ("my:")
        print rid_me,bid_me
        print ("yi's:")
        print rid_me,bid_yi
        break
