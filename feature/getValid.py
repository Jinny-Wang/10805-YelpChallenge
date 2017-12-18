# tag reviews after 2016-01-01 (4180) as 1; 0 otherwise
import csv
import sys

def getValid():
	print("Start tagging.....")
	with open("/Users/yixu/Desktop/yelp/feature/dataset/full/time_elapse.csv", 'r') as in_file:
		with open("/Users/yixu/Desktop/yelp/feature/dataset/full/validReviews.csv", 'w') as out_file: 
			total = 0
			writer=csv.writer(out_file, delimiter='\t',lineterminator='\n',)
			for row in in_file:
				# print row
				row = row.split()
				date = int(row[2])
				isValid = 1 if date < 4180 else 0
				# print isValid
				towrite = [row[0], row[1], row[2], isValid]
				# print towrite
				writer.writerow(towrite)
				total += 1
				if total % 5000 == 0:
					print "Finish " + str(total)



if __name__ == "__main__":
	getValid()