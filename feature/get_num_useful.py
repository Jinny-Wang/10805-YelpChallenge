import csv
# get the useful proportion of reviews among all the reviews

full_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/labels_full_validated.csv"

def get_num_useful(): 
	with open(full_path, 'r') as f: 
		reader = csv.reader(f, delimiter = '\t')
		useful, not_useful = 0, 0
		count = 0
		for row in reader: 
			u_score = float(row[-2])
			isValid = int(row[-1])
			# if valid, i.e. if before 2016.01.01
			if isValid: 
				if u_score > 0: 
					useful += 1
				else:
					not_useful += 1
			count += 1
			if count % 50000 == 0: 
				print "finished " + str(count)
		print "useful ", useful 
		print "not_useful", not_useful
		print "use_ful proportion", float(useful) / (useful + not_useful) 

if __name__ == "__main__": 
	get_num_useful()