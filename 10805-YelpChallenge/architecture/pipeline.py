import json
import numpy as np
from numpy import genfromtxt
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import roc_curve
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn.model_selection import train_test_split
import string
import logger
import csv
import sys
import nltk
from nltk import word_tokenize
from sklearn.neural_network import MLPClassifier

#This is the pipeline for training subset of yelp data
#Only work for 30 wan subset
path_label = "/Users/yuyanzhang/Desktop/CMU/10605/yelp/10805-YelpChallenge/config/sub_label_validated.csv"
path_split = "/Users/yuyanzhang/Desktop/CMU/10605/yelp/10805-YelpChallenge/config/"
root_path_feature = "/Users/yuyanzhang/Desktop/CMU/10605/yelp/10805-YelpChallenge/feature/"
model_name = ""
info = ""
#Load labels for subset
#Label file should be stored in the format of [id, row, label]
#The function returns only the label column

def load_data_valid(path):
	with open(path, 'rb') as f:
		reader = csv.reader(f,delimiter='\t')
		labels = np.array((list)(reader))
	return labels[:,3]



def load_label(path, valid, num_class = 3):
	with open(path, 'rb') as f:
	    reader = csv.reader(f,delimiter='\t')
	    labels = np.array((list)(reader))
	label = []
	idx = []
	if num_class == 2:
		for y in labels:
			if y[2] == '2' or y[2] == '1':
				label.append(1)
			else:
				label.append(0)
			idx.append(y[0])
	else:
		label = labels
		idx = y[:,0]

	rt = []
	valid_idx = []
	for i in range(len(label)):
		if (int)(valid[i]) == 0:
			continue
		else:
			rt.append(label[i])
			valid_idx.append(idx[i])
	print("labels loaded")
	return np.array(rt),np.array(valid_idx)



#Change this function to apply different smoothing function to the days elapsed
#Accept numpy array
def prep_days_elapsed(days):
	constant = 1
	return np.log(days.astype(np.float))*constant

#Load features
#The first column of all feature files should be the id of the datapoint
#The function return everything except for the id column
def load_feature(feature,valid):
	print("Loading feature: ",feature)
	path = "".join([root_path_feature,feature,".csv"])
	rt = []
	with open(path, 'rb') as f:
	    reader = (list)(csv.reader(f,delimiter='\t'))
	    count = 0
	    for row in reader:
	    	if (int)(valid[count]) == 0:
	    		pass
	    	else:
	    		rt.append(row[1:len(row)])
	    	count += 1
	print(feature," Loading finished")
	return np.array(rt)


#Change this function to experiment with different modeling technique
#Be sure to change the info in the logger to log results for different model/feature space
def cross_val(X,target,fold):
	my_logger = logger.logger()
	print("Cross validating")
	#clf = svm.SVC(kernel='linear', C=1)
	clf = RandomForestClassifier()
	print(str(len(target)), "datapoints")
	scores = cross_val_score(clf, X, target, cv=fold,n_jobs=10, scoring='accuracy')
	print("accuracy",np.mean(scores))
	#####Log the currenet model info#####
	print(info)
	my_logger.log_model(model_name,clf,np.mean(scores),info=info)



def model_experiment():
	valid = load_data_valid(path_label)
	target = load_label(path_label,valid, num_class=2)[0]

	print("model name")
	model_name = raw_input()
	print("info")
	info = "".join([raw_input(),'\n'])
	
	text_meta = load_feature("review_text_meta", valid)
	time = prep_days_elapsed(load_feature("review_time_elapse", valid))
	bus_meta = load_feature("business_meta", valid)

	#Combine all features into a bigger feature space
	X = np.c_[text_meta,time,bus_meta]
	cross_val(X,target,5)


#X: [id, x1, x2...]
#target: [id, label]
def train_test_split(X,target):
	print("Split training and testing set")
	train_idx = np.load("".join([path_split,"x_train.npy"]))
	test_idx = np.load("".join([path_split,'x_test.npy']))
	train_lookup = {key: 1 for key in train_idx}
	test_lookup = {key: 0 for key in test_idx}

	lookup = dict(train_lookup, **test_lookup)

	x_train = np.array([x for x in X if lookup[x[0]]==1])
	x_test = np.array([x for x in X if lookup[x[0]]==0])

	y_train = np.array([y for y in target if lookup[y[0]]==1])
	y_test = np.array([y for y in target if lookup[y[0]]==0])
	return x_train[:,1:len(x_train)],x_test[:,1:len(x_test)],y_train[:,1:len(y_train)].reshape(len(y_train),),y_test[:,1:len(y_test)], y_test[:,0]


def model_fit():
	print("model name")
	model_name = raw_input()
	print("info")
	info = "".join([raw_input(),'\n'])

	valid = load_data_valid(path_label)
	target = load_label(path_label,valid, num_class=2)[0]
	idx = load_label(path_label,valid, num_class=2)[1]
	print(len(target))
	
	text_meta = load_feature("review_text_meta", valid)
	time = prep_days_elapsed(load_feature("review_time_elapse", valid))
	bus_meta = load_feature("business_meta", valid)
	brain_hole = load_feature("sent_meta",valid)

	#Combine all features into a bigger feature space
	X = np.c_[idx,text_meta,time, bus_meta,brain_hole]

	y = np.c_[idx,target]

	x_train,x_test,y_train,y_test, idx_test = train_test_split(X,y)

	#clf = RandomForestClassifier()
	# clf = svm.SVC(kernel='linear', C=1)
	clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)
	print("Fitting modeling")
	clf.fit(x_train,y_train)
	print("Predicting")
	pred = clf.predict(x_test)
	print("Accuracy")
	print(accuracy_score(pred, y_test))
	my_logger.log_model(model_name,clf,accuracy_score(pred, y_test),info=info)

	# pred = clf.predict_proba(x_test)
	# # 
	# # 
	# #Write pred to file
	# out = np.c_[idx_test,pred]
	# print(out)
	# np.save(open("../log/pred_prob_with_busmeta.npy",'w'), out)

	print("Done")





if __name__ == '__main__':
	#model_experiment()
	model_fit()













