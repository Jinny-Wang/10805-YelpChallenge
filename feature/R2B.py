import json
import sys
import csv
'''
Craete an inverted index map from review_id to a list of business_id
'''

feature_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/full_feature.csv"
out_dir = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/"
R2B = {}

def build_dic():
	with open(feature_path, 'r') as f: 
		with open(''.join([out_dir, 'R2B.json']), 'w') as out_file: 
			for row in f: 
				row = row.split()
				r_id, b_id = row[0], row[1]
				R2B.setdefault(r_id, []).append(b_id)
			json.dump(R2B, out_file)

if __name__ == "__main__": 
	build_dic()