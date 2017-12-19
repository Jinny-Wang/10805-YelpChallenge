
#distance up to 1
import csv
import numpy as np
import json
import sys
X = []
count = 0

D = 6 #up to distance 5
dist = [i for i in range(2,D+1)] 

for d in dist:
    filename = "_".join(['review_word_comb_distance',str(d)])
    outname = "_".join(['review_word_comb_distance',str(d),'_reduce'])
    x = []
    count = 1
    feature_set = []

    dict_file = "".join([str(d-1),"_word_comb_dict.txt"])
    with open(dict_file) as json_data:
        feature_dict = json.load(json_data)


    for k,v in feature_dict.iteritems():
        if v > 1000:
            feature_set.append(k)
    feature_size = len(feature_set)
    feature_set = set(feature_set)
    print(feature_size)

    with open(outname,'w') as out:
        writer = csv.writer(out,delimiter='\t')
        writer.writerow(x)

    with open(filename, 'rb') as f:
        reader = csv.reader(f,delimiter='\t')
        with open(outname,'a') as out:
            for row in reader:
                count += 1
                if (count %10000 ==0):
                    print(count)
                #x = [comb for comb in row if comb in feature_set]
                x = list(set(row) & feature_set)
                writer = csv.writer(out,delimiter='\t')
                writer.writerow(x)
            
