import csv
import sys
import itertools as IT
'''
full_feature.csv format
[busi_path, text_path, sent_path, time_path, label_path]
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

busi_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/business_meta.csv"
text_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/text_meta.csv"
sent_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/sent_meta.csv"
time_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/time_elapse.csv"
label_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/labels_full_validated.csv"
out_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/full_feature.csv"

in_paths = [busi_path, text_path, sent_path, time_path, label_path]
handles = [open(in_path, 'rb') for in_path in in_paths] 
readers = [csv.reader(f, delimiter=',') for f in handles]

def merge_features(): 
	print ("start combining")
	with open(out_path, 'wb') as out_file: 
		writer=csv.writer(out_file, delimiter='\t',lineterminator='\n',)
		count = 0
		for rows in IT.izip_longest(*readers, fillvalue=['']*2):
			combined_row = []
			for row in rows:
				row = row[0].split() 
				if len(combined_row) != 0:
					combined_row += row[2:]
					# print combined_row
				else: 
					combined_row = row
					# print combined_row
			count += 1
			if count % 50000 == 0: 
				print "Finished" + str(count)
			# print combined_row
			# print "final " + str(combined_row)
			writer.writerow(combined_row)


if __name__ == "__main__":
	merge_features()