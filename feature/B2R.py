import json
import sys
import csv
'''
Craete an inverted index map from business_id to a list of review_ids
'''

feature_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/full_feature.csv"
out_dir = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/"
B2R = {}

def build_dic():
	with open(feature_path, 'r') as f: 
		with open(''.join([out_dir, 'B2R.json']), 'w') as out_file: 
			for row in f: 
				row = row.split()
				r_id, b_id = row[0], row[1]
				B2R.setdefault(b_id, []).append(r_id)
			json.dump(B2R, out_file)

if __name__ == "__main__": 
	build_dic()