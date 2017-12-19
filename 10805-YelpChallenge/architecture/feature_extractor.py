#import ConnectToSQLServer
import csv
import numpy as np
from numpy import genfromtxt
from nltk import word_tokenize,pos_tag

##############Configurations###############
subset_path = "../config/labels.csv"
##############End Configurations###############
#

#Load subset of the data for training
def load_subset(path):
	data = genfromtxt(path, delimiter='\t',dtype=None)
	return data

#Return [id, review]
def query_review_text(cnx):
	cursor = cnx.cursor()
	query = ("SELECT id,text FROM review")
	cursor.execute(query) 
	results = cursor.fetchall()
	print("Date diff finished")
	return results

def query_datediff(cnx):
	cursor = cnx.cursor()
	query = ('select id,DATEDIFF((review.date), "2004-07-22 00:00:00") from review')
	cursor.execute(query) 
	results = cursor.fetchall()
	print("Review text query finished")
	return results

def extract_text_meta(labels, cursor):
	count = 0
	subset_count = 0
	result = query_datediff(cursor)
	with open('../feature/review_text_meta.csv','w') as f1:
		writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
		for row in result:
			row_id = row[0]
			review = row[1]

			count += 1
			if count%50000 == 0:
				print("".join([(str)(count),"total data scanned"]))
			
			if count != labels[subset_count][1]:
				continue
			elif row_id != labels[subset_count][0]: #Check to see if ids match
				continue
			else:
				subset_count += 1
				#Current data is in the subset, process current data sample
			
		        if (subset_count %10000 == 0): #Print process every 10000 data points
		            print("".join([(str)(subset_count),"subset data point processed"]))

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
		        towrite = [row_id,num_token, num_noun, num_verb, num_adj, num_adverb,
		                  num_exclaimation, num_question,num_upper]
		        writer.writerow(towrite)
                
	print("Done extracting meta data features from the review text")

#Return number of days elapsed from the post date of current review to the day 1 in the dataset
def query_timestamp(lables, cursor):
	#results = query_review_text(cursor)
	with open('../feature/days_elapsed.csv', 'rb') as f:
	    reader = csv.reader(f,delimiter='\t')
	    results = np.array((list)(reader))

	count = 0
	subset_count = 0
	with open('../feature/review_time_elapse.csv','w') as f1:
		writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
		for row in results:
			days = row[0]
			count += 1
			if count%50000 == 0:
				print("".join([(str)(count),"total data scanned"]))
			if subset_count == len(results):
				break
			if count != labels[subset_count][1]:
				continue
			# elif row_id != labels[subset_count][0]: #Check to see if ids match
			# 	continue
			else:
				subset_count += 1
				#Current data is in the subset, write to file
				row_id = lables[0]
				writer.writerow([row_id,days])
		        if (subset_count %10000 == 0): #Print process every 10000 data points
		            print("".join([(str)(subset_count),"subset data point processed"]))
	print("Done writing time stamps to file")
	return results


#Query the meta data of use and business info associated with each review post
def query_business(lables, cnx):
	print("Quering business meta data")
	count = 0
	cursor = cnx.cursor()
	with open('../feature/business_meta.csv','w') as f:
		writer=csv.writer(f, delimiter='\t',lineterminator='\n')
		for y in labels:
			count += 1
			if count % 5000 == 0:
				print(count)
			id = y[0]
			query = ("select sample.review_id, b.id,sample.ind, b.review_count, b.stars, b.state,b.latitude,b.longitude,b.postal_code, group_concat(c.category) from review " +
				"where review_"+
				"left join business as b on b.id = review.business_id left join category as c on c.business_id = review.business_id " +
				"left join sample on sample.review_id =review.id group by c.business_id limit 100;")
	cursor.execute(query) 
	results = cursor.fetchall()
	print("business meta data finished")
	return results

#If a review is posted after 2016, do not use it for training
def query_valid_data(labels, cnx):
	print("Get data time validation")
	count = 0
	cursor = cnx.cursor()
	with open('../config/label_validated.csv','w') as f:
		writer=csv.writer(f, delimiter='\t',lineterminator='\n')
		for y in labels:
			count += 1
			if count %5000 == 0:
				print(count)
			id = y[0]
			query = ('select if(date>"2016-01-01 00:00:00", 0, 1) from review where id = %s ; ')
			cursor.execute(query, ((str)(id), ))
			result = cursor.fetchall()
			for r in result:
				valid = r[0]
			y = (list)(y)
			towrite = y + [valid]
			writer.writerow(towrite)
		print("Done")

def get_valid_data(labels):
	with open('../config/all_label_valid.csv', 'rb') as f:
	    reader = csv.reader(f,delimiter=',')
	    next(reader, None)
	    results = np.array((list)(reader))
	count = 0
	subset_count = 0
	print("Getting valid data")
	with open('../config/sub_label_validated.csv','w') as f1:
		writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
		for row in results:
			count += 1
			if count%50000 == 0:
				print("".join([(str)(count),"total data scanned"]))
			if subset_count == len(results):
				break
			if count != labels[subset_count][1]:
				continue
			# elif row_id != labels[subset_count][0]: #Check to see if ids match
			# 	continue
			else:
				
				#Current data is in the subset, write to file
				towrite = (list)(labels[subset_count]) + [row[2]]
				writer.writerow(towrite)
		        if (subset_count %10000 == 0): #Print process every 10000 data points
		            print("".join([(str)(subset_count),"subset data point processed"]))
		        subset_count += 1
	print("Done getting valid data")
	return results

def sent_meta(labels):
	with open('../feature/text_meta_sent_length.csv', 'rb') as f:
	    reader = csv.reader(f,delimiter='\t')
	    results = np.array((list)(reader))

	count = 0
	subset_count = 0
	with open('../feature/sent_meta.csv','w') as f1:
		writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
		for row in results:
			id = row[0]
			count += 1
			if count%50000 == 0:
				print("".join([(str)(count),"total data scanned"]))
			if subset_count == len(results):
				break
			if count != labels[subset_count][1]:
				continue
			# elif row_id != labels[subset_count][0]: #Check to see if ids match
			# 	continue
			else:
				subset_count += 1
				#Current data is in the subset, write to file
				row_id = labels[0]
				writer.writerow(row)
		        if (subset_count %10000 == 0): #Print process every 10000 data points
		            print("".join([(str)(subset_count),"subset data point processed"]))
	print("Done sent meta stamps to file")
	return results


if __name__ == '__main__':
	#Connect to the sql server
	#c = ConnectToSQLServer.connect()
	labels = load_subset(subset_path)
	#data = query_review_text(cnx)
	#extract_text_meta(cursor)
	#query_timestamp(labels,cnx)
	#query_valid_data(labels, c)
	# get_valid_data(labels)
	sent_meta(labels)