import sys
import json
import math

'''
call python pipeline.py filename

filename: full_feature, food, health, etc. 
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

cate_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/businessid_category.json"
R2B_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/R2B.json"
B2R_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/B2R.json"
dir_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/clusters/"

MAX_DEPTH = 3
MAX_FEATURES = 6

# row[0] row[1] should be the review id and business id respectively
# the function should return everything except for the two ids
# log the elapse time
def parse(row):
	for i in range(2, len(row)): 
		row[i] = float(row[i])
	if row[18] > 0:
		row[18] = math.log(row[18])
	return row[2:]

def getCate(u):
		return 0 if u == 0 else 1

def model_fit(category): 
	with open(''.join([dir_path, category, '.csv'])) as csv_file: 
		reader = csv.reader(csv_file, delimiter = '\t')
		# X is N by M = 17, where M is the num of features and N is the number of training examples
		X = []
		# Y is N by 1, format of each row: [usefulness_score]
		Y = []
		print "loading data ---------------------"
		count = 0
		for row in reader: 
			row = parse(row)
			# if not valid
			if not row[-1]: 
				continue
			# print "isValid", row[-1]

			useful = getCate(row[-2])
			# print "usefulness score", useful
			# preserve only the feature values in a vector
			row  = row[:-2]
			X.append(row)
			Y.append([useful])
			# print X
			# print Y

			count += 1
			# if count >= 5: 
			# 	break
			if count % 50000 == 0: 
				print "finished " + str(count)

		X = np.array(X)
		Y = np.array(Y)
		X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.1, random_state = 34)

		print "-------------start training--------------"
		clf = tree.DecisionTreeClassifier(max_depth=MAX_DEPTH,max_features=MAX_FEATURES)
		clf.fit(X_train, Y_train)

		# print "training feature***********************"
		# print X_train.shape
		# print "training label*************************"
		# print Y_train.shape
		# print "testing feature************************"
		# print X_test.shape
		# print "testing label**************************"
		# print Y_test.shape

		print "-------------start predicting---------------"
		X_train = X_train.tolist()
		Y_train = Y_train.tolist()
		X_test = X_test.tolist()
		Y_test = Y_test.tolist()

		train_pred = clf.predict(X_train)
		test_pred = clf.predict(X_test)
		print "-------------finish predicting---------------"

		train_f1 = f1_score(Y_train, train_pred, average = None)
		test_f1 = f1_score(Y_test, test_pred, average = None)
		train_accuracy = accuracy_score(Y_train, train_pred)
		test_accuracy = accuracy_score(Y_test, test_pred)
		train_recall = recall_score(Y_train, train_pred, average = None)
		test_recall = recall_score(Y_test, test_pred, average = None)
		train_precision = precision_score(Y_train,train_pred,average=None)
		test_precision = precision_score(Y_test,test_pred,average=None)
		print category
		print "train_f1 " + str(train_f1)
		print "test_f1 " + str(test_f1)
		print "train_accuracy " + str(train_accuracy)
		print "test_accuracy " + str(test_accuracy)
	return 


if __name__ == "__main__": 
	category = sys.argv[1]
	model_fit(category)