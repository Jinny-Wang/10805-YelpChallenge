import csv
import json

feature_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/full_feature.csv"
cate_path = "/Users/yixu/Desktop/yelp/feature/dataset/full/meta/businessid_category.json"
out_dir = "/Users/yixu/Desktop/yelp/feature/dataset/full/clusters/"
  
def get_cate_dir(): 
	with open(cate_path, 'r') as cate_f: 
		cate_dir = json.loads(cate_f.readline())
	return cate_dir

def split_by_cate(): 
	# business_id : category
	cate_dir = get_cate_dir() 
	clustername = {'Active Life':'active_life',
	'Arts & Entertainment':'arts&ent','Automotive':'auto','Beauty & Spas':'beauty&spas','Education':'edu',
                'Event Planning & Services':'service','Fashion':'fasion','Financial Services':'finance','Food':'food','Grocery':'grocery',
                'Health & Medical':'health','Home & Garden':'home&garden','Home Services':'home_service','Hotels & Travel':'hotel&travel','Nightlife':'nightlife',
                'Pets':'pets','Real Estate':'real_estate','Shopping':'shopping'}

	handles = {f : open(''.join([out_dir, clustername[f], '.csv']), 'wb') for f in clustername.keys()}
	# print handles
	writers = {f : csv.writer(handles[f], delimiter='\t',lineterminator='\n',) for f in handles}
	# print writers

	count = 0
	with open(feature_path, 'r') as fea_f:
		print "start write....."
		for row in fea_f: 
			business_id = row.split()[1]
			cates = cate_dir.get(business_id, "Not Found")
			# print cates
			for cate in cates: 
				if writers.has_key(cate): 
					writer = writers[cate]
					# print row
					writer.writerow([row])

			count += 1
			if not count % 50000: 
				print "Finished " + str(count)


if __name__ == "__main__": 
	split_by_cate()