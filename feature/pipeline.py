import sys
import json

'''
写让自己自豪的代码
做让自己开心的事情
嘻嘻嘻
'''
'''
Predict usefulness score in the specified category with the metadata of business, reviews, and users. 

[0]review_id, 
[1]business_id, 
[2]longitude, 
[3]latitude, 
[4]rating, 
[5]review_count, 
[6]Num_token, 
[7]num_noun, 
[8]num_verb, 
[9]num_adj, 
[10]num_adverb, 
[11]num_!, 
[12]num_?, 
[13]num_upper
[14]Number of sentences with <=30 tokens, 
[15]number of sentences with > 30 tokens, 
[16]average sentence length, 
[17]sent_count, 
[18]elapse_time, 
[19]usefulness_score, 
[20]isValid
'''
import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn import svm
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score 
from sklearn import tree

clustername = {'Active Life':'active_life',
'Arts & Entertainment':'arts&ent','Automotive':'auto','Beauty & Spas':'beauty&spas','Education':'edu',
              'Event Planning & Services':'service','Fashion':'fasion','Financial Services':'finance','Food':'food','Grocery':'grocery',
              'Health & Medical':'health','Home & Garden':'home&garden','Home Services':'home_service','Hotels & Travel':'hotel&travel','Nightlife':'nightlife',
              'Pets':'pets','Real Estate':'real_estate','Shopping':'shopping'}

# row[0] row[1] should be the review id and business id respectively
# the function should return everything except for the two ids
# log the elapse time
def load_feature(row): 

	return row


def model_fit(category = 'food'): 
	return 






if __name__ == "__main__": 
	category = sys.argv[1]
	model_fit(category)