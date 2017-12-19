####Convert word combination tokens to bag of words representation####
import sys
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re
import json
import csv

##########Configuration#########
d = sys.argv[1] #Change d to process difference distance 

#Change infile and outfile name if necessary
infile = "".join(["review_word_comb_distance_",str(d),"__reduce"])
outfile = "".join([str(d),"dist_bow.csv"])
#################################
def tokenize(text):
    return(re.split('\t',text.strip()))

#Load the feature set
dict_file = "".join([str((int)(d)-1),"_word_comb_dict.txt"])
with open(dict_file) as json_data:
    feature_dict = json.load(json_data)

feature_set = []
for k,v in feature_dict.iteritems():
    if v > 4000:
        feature_set.append(k.encode('utf-8').strip())
feature_size = len(feature_set)
feature_set = list(set(feature_set))
feature_set = {k: v for v, k in enumerate(feature_set)}
print(feature_size)


#Vectorized matrix for bag of word representation

#For now, only vectorize the subset of data
#Read in the index for all subsets
subset_idx = []
with open('labels.csv','r') as f:
  reader = csv.reader(f,delimiter='\t')
  for line in reader:
    # if (int)(line[2]) == 1:
    subset_idx.append(int(line[1]))
subset_idx = sorted(subset_idx)
print("Total subset: ", len(subset_idx))

count = 0
with open(infile,'rb') as f:
  reader = csv.reader(f,delimiter='\t')
  with open(outfile,'w') as o:
    writer = csv.writer(o,delimiter='\t')
    #writer.writerow(feature_set)
    for line in f:
      count += 1
      # if count not in subset_idx:
      #   pass
      if count %1000 ==0:
        print(count)
        #break
      line = tokenize(line)
      row = np.zeros(feature_size)
      for item in row:
        if feature_set.has_key(item):
          row[feature_set[item]] = 1
      writer.writerow(row)
