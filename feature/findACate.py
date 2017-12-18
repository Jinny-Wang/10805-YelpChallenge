import json
import sys
import csv

# given a review id, find its category
# find cXwxcRzNCUrZxId-GiOVhg
# find tJgNO-rjPuaSPBktsXN11w

cate_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/businessid_category.json"
R2B_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/R2B.json"

def get_dic(path): 
	with open(path, 'r') as f: 
		dic = json.loads(f.readline())
	return dic


if __name__ == "__main__":
	to_check = sys.argv[1]
	cate_dic = get_dic(cate_path)
	R2B_dic = get_dic(R2B_path)
	# print cate_dir
	print "size of cate_dir " + str(len(cate_dic))
	print "size of R2B_dir " + str(len(R2B_dic))
	busi_id = R2B_dic.get(to_check, ["Not found"])[0]
	print "business_id : " + str(busi_id)

	if busi_id != "Not found": 
		print "categoris are " + str(cate_dic.get(busi_id, "No cate"))

