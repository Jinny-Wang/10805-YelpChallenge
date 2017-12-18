#Following features will be extracted:
#text_meta,time, bus_meta
#Features will be stored in the format of [id, feature space]
import csv
import numpy as np
from numpy import genfromtxt
from nltk import word_tokenize,pos_tag,sent_tokenize
import sys

import json

def extract_text_meta(name):
	print("Quering text meta data")
	with open(''.join(["/Users/yixu/Desktop/yelp/feature/dataset/", name]),'r') as f:
		with open(''.join(['/Users/yixu/Desktop/yelp/feature/result/',name,'.csv']),'w') as f1:
			writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
			count = 0
			subset_count = 0
			
			for row in f:
				#print(row)
				row = json.loads(row)
				review_id = row['review_id']
				buz_id = row['business_id']
				review = row['text']

				count += 1
				if count%50000 == 0:
					print("".join([(str)(count),"total data scanned"]))
				
		
				review = word_tokenize(review)

				#Number of tokens
				num_token = (float)(len(review))
				row_pos_tag = pos_tag(review)
				#Number of nouns, verbs, adjectives, and adverbs
				num_noun = len([token for token,pos in row_pos_tag if pos.startswith('N')])
				num_verb = len([token for token,pos in row_pos_tag if pos.startswith('V')])
				num_adj = len([token for token,pos in row_pos_tag if pos.startswith('J')])
				num_adverb = len([token for token,pos in row_pos_tag if pos.startswith('R')])
				#Number of words starting with uppercase
				num_upper = 0
				#Number of ! and ?
				num_exclaimation = 0
				num_question = 0
				for token in review:
					if token[0].isupper():
						num_upper += 1
					elif token == "!":
						num_exclaimation += 1
						num_question += 1
				#Compute the ratio of each feature and total number of tokens
				towrite = [review_id,buz_id,num_token, num_noun, num_verb, num_adj, num_adverb,
						  num_exclaimation, num_question,num_upper]
				#print(towrite)
				writer.writerow(towrite)


if __name__ == '__main__':
	name = sys.argv[1]
	extract_text_meta(name)
