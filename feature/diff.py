import csv
import sys


dir_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/clusters/"
## print the different review id in f1 and f2
def diff(f1, f2): 
	with open(''.join([dir_path, f1]), 'r') as file1, open(''.join([dir_path, f2]), 'r') as file2: 
		id_list = []

		for row in file1: 
			r_id = row.split()[0]
			id_list.append(r_id)

		id_set = set(id_list)
		# if len(id_set) != set(id_list): 
		# 	print "id_list have duplicate!"
			# print len(id_set)
			# print len(id_list)

		diff_id = []
		for row in file2:
			r_id = row.split()[0]
			if r_id not in id_set: 
				diff_id.append(r_id)
		print diff_id
		# print len(diff_id)
	return 



if __name__ == "__main__": 
	f1 = sys.argv[1]
	f2 = sys.argv[2]
	diff(f1, f2)