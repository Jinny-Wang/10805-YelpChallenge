import csv
import numpy as np
import sys
import json

## x_pos and x_neg is raw data fed to CNN when trianing
x_pos = open("./useful_validated_withid.pos",'r')
x_neg = open("./notuseful_validated_withid.neg",'r')

## x_test: the review id of test data set sent to amber
x_test = np.load("./x_test.npy")

## load predictions for random forest model and cnn model
rv_pred_score = np.load('./pred_prob_with_busmeta.npy')
#cnn_pred  = np.load('./cnnprediction.npy')
cnn_pred_score = np.load('./cnnprediction_prob.npy')
## weight for random forest model
rv_weight = float(sys.argv[1])
cnn_weight = 1-rv_weight

## combined >= cutoff -> output 1
cutoff = float(sys.argv[2])
print "rv_pred.shape",rv_pred_score.shape
print "cnn_pred.shape",cnn_pred_score.shape
print "size of test",x_test.shape

## The following code is for double checking only!#############################
labels_cnn = dict()
review_len_distribution  = dict()
for line in x_pos:
    line = line.split('\t')
    labels_cnn[line[0]] = 1
    size  = len(line[1].split())
    if size in review_len_distribution:
        review_len_distribution[size]+=1
    else:
        review_len_distribution[size]=1
for line in x_neg:
    line = line.split('\t')
    labels_cnn[line[0]] = 0
    size  = len(line[1].split())
    if size in review_len_distribution:
        review_len_distribution[size]+=1
    else:
        review_len_distribution[size]=1
print review_len_distribution
with open("review_len.json",'w') as fp:
    json.dump(review_len_distribution,fp)

## labels dict prestored from labels_validated_updated.csv
with open("labelsdict.json",'r') as fp:
    labels = json.load(fp)
print "size of labels_cnn",len(labels_cnn)
print "size of validated labels",len(labels)

## difference between labels used for cnn and labels used in rv model
## if diff is not empty-> there must be some problem!
diff = set(labels.keys()) - set(labels_cnn.keys())
print "size of difference",len(diff)

for key in labels:
    if key not in labels_cnn:
        print "key not consistent!"
        print key
    if labels[key] != labels_cnn[key]:
        print "label inconsistent!"
        print key
        break
########################### END of double checking ############################

x_test_id = dict()
for idx in x_test:
    x_test_id[idx] = 1

cnn_pred_dict = dict()
for i in range(len(cnn_pred_score)):
    if cnn_pred_score[i][0] in x_test_id:
        cnn_pred_dict[cnn_pred_score[i][0]] = float(cnn_pred_score[i][1]) ## key : reviewid , value : positive label probability
print "size of cnn_pred_dict on test set",len(cnn_pred_dict)

rv_pred_dict = dict()
for i in range(len(rv_pred_score)):
    if rv_pred_score[i][0] in x_test_id:
        rv_pred_dict[rv_pred_score[i][0]] = float(rv_pred_score[i][2])
print "size of rv_pred_dict on test set",len(rv_pred_dict)

### this is very dirty : delete the keys that are in rv but not in cnn ######
### just a rude way to match things up ######################################
### TODO: further check why the keys are not matching #######################
### e.g. are we really using the same data for training/testing? ###########
diff2 = set(rv_pred_dict.keys())- set(cnn_pred_dict.keys())
for key in diff2:
    del rv_pred_dict[key]

### combinePred : generate prediction given scores from two models and their weights##
def combinePred(rv_weight,cnn_weight,rv_pred,cnn_pred,cutoff):
    score = rv_weight*rv_pred + cnn_weight*cnn_pred
    if(score >= cutoff):
        return 1
    else:
        return 0

def scoreToPred(score):
    if (score>=0.5):
        return 1
    else:
        return 0

correct = 0
TP = 0
TN = 0
FP = 0
FN = 0
only_rv_correct = {1:0,0:0}
only_cnn_correct = {1:0,0:0}
only_rv_id  = []  ## review id where only rv model predicted correctly
only_cnn_id  = [] ## review id where only cnn model predicted correctly
only_rv_csv = csv.writer(open("only_rv_prob.csv",'w'),delimiter=',')
only_cnn_csv = csv.writer(open("only_cnn_prob.csv",'w'),delimiter=',')

for key in rv_pred_dict:
    rv_pred_prob = rv_pred_dict[key]
    cnn_pred_prob = cnn_pred_dict[key]
    final_pred = combinePred(rv_weight,cnn_weight,rv_pred_prob,cnn_pred_prob,cutoff)
    if key not in labels:
        print "id not included! something wrong"
        break
    if final_pred == labels[key]:
        correct += 1
        if final_pred==1:
            TP+= 1
        else:
            TN += 1
    else:
        if final_pred==1:
            FP+=1
        else:
            FN+=1
    rv_pred = scoreToPred(rv_pred_prob)
    cnn_pred = scoreToPred(cnn_pred_prob)
    if rv_pred != cnn_pred:
        if(labels[key] == rv_pred):
            only_rv_correct[rv_pred] +=1
            only_rv_id.append(key)
            only_rv_csv.writerow([key,rv_pred_prob,rv_pred])
        if(labels[key]== cnn_pred):
            only_cnn_correct[cnn_pred] += 1
            only_cnn_id.append(key)
            only_cnn_csv.writerow([key,cnn_pred_prob,cnn_pred])

acc  = float(correct)/len(rv_pred_dict)
precision = float(TP)/float(TP+FP)
recall = float(TP)/float(TP+FN)
print ("Accuracy is %f " %(acc))
print ("Precision is %f"%(precision))
print ("Recall is %f"%(recall))

print ("only rv correct",only_rv_correct )
print ("only cnn correct",only_cnn_correct )
