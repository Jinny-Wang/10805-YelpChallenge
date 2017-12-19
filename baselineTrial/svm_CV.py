## 10-805 Machine Learning with Large Dataset  Final Project
## Yelp Challenge
## Author: Yi Xu

import csv
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split
from sklearn import svm
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score 
from sklearn.neural_network import MLPClassifier



# to explore the correlation between review usefulness
# and some metadata like the fans of the user
# the elite years of the user
# the number of friends of the user
# the total compliment recieved by the user

def getCate(u):
		if u == 0: 
			return 0
		elif u <= 7: 
			return 1
		else: 
			return 2
		# if u == 0:
		# 	return 0
		# else: 
		# 	return 1

def parse(line): 
	for i in range(5, len(line)): 
		line[i] = int(line[i])
	line[3] = int(line[3])
	# only reserving the year (the first four digit) 
	line[4] = int(line[4][:4])
	return line



with open('metaFeature.csv', 'r') as csvfile: 
	reader = csv.reader(csvfile, delimiter = ';')
	feature_list = reader.next()
	# print feature_list
	line = parse(reader.next())
	X = [line[4:]]
	useful = int(line[3])
	Y = [getCate(useful)]
	# print X
	# print Y

	print "-------------loading data----------------"
	for row in reader:  
		row = parse(row)
		X.append(row[4:])
		useful = int(row[3])
		Y.append(getCate(useful))

	X = np.array(X)
	Y = np.array(Y)
	print "-------------start training--------------"

	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.33, random_state = 34)
	# clf = GaussianNB()
	# clf = svm.SVC(kernel = 'rbf')
	clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
	clf.fit(X_train, Y_train)

	print "training feature***********************"
	print X_train.shape
	print "training label*************************"
	print Y_train.shape
	print "testing feature************************"
	print X_test.shape
	print "testing label**************************"
	print Y_test.shape



	total = 0
	miss = 0
	print "-------------start predicting---------------"
	X_train = X_train.tolist()
	Y_train = Y_train.tolist()
	X_test = X_test.tolist()
	Y_test = Y_test.tolist()

	train_pred = clf.predict(X_train)
	test_pred = clf.predict(X_test)
	print "-------------finish predicting---------------"

	# train_f1 = f1_score(Y_train, train_pred, average = None)
	# test_f1 = f1_score(Y_test, test_pred, average = None)
	train_accuracy = accuracy_score(Y_train, train_pred)
	test_accuracy = accuracy_score(Y_test, test_pred)
	# train_recall = recall_score(Y_train, train_pred, average = None)
	# test_recall = recall_score(Y_test, test_pred, average = None)
	# train_precision = precision_score(Y_train,train_pred,average=None)
	# test_precision = precision_score(Y_test,test_pred,average=None)
	# print "train_f1 " + str(train_f1)
	# print "test_f1 " + str(test_f1)
	print "train_accuracy " + str(train_accuracy)
	print "test_accuracy " + str(test_accuracy)	