### Yelp Challenge
### December 16th 2017
### Jingyu Wang

### cluster_reviews.py
### Dependency : 1. /Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/10805-YelpChallenge/config/category_cluster.json
###              2. Format    {general_category1 : [business_id1, business_id2, ... , business_idn], general_category2 : [business_id1,business_id2,...,business_idn]}


import json
import csv
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string


## not used here
## connect to the mysql server
def connect():
    # step 1 : connect to the remote MySQL server
    try:
      cnx = mysql.connector.connect(user='Admin10805', password='10805fall2017',
                                  host='yelp2.csfuygoxtob2.us-east-2.rds.amazonaws.com',
                                  database='yelp_db')
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    return cnx
    # else:
    #   cnx.close()

def main():
    category_cluster_filename = "/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/10805-YelpChallenge/config/category_cluster.json"
    rawonegram_filename = "/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/rawNgram/1gram.csv"
    #TODO : complete the filename here
    reviews_filename = "/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/extractNgram_labels/review_token_augmented.csv"
    category_cluster_dict = dict() # category -> list of business ids
    with open(category_cluster_filename,'r') as fp:
        category_cluster_dict = json.load(fp)

    ## output file, store review id and review text in each file
    category_file = dict() # open output file for each cluster
    for k in category_cluster_dict: # key : category, value : opened file
        category_file[k] = open( k+".txt",'w')

    ## get the reversed dictionary : business_id -> categories
    businessid_cate = dict() # dictionary business_id -> list of categories
    for category in category_cluster_dict:
        for business in category_cluster_dict[category]:
            if business in businessid_cate:
                businessid_cate[business].append(category)
            else:
                businessid_cate[business] = [category]

    ## store the reversed dictionary (bid->categories)
    with open("businessid_category.json",'w') as bid_cat:
        json.dump(businessid_cate,bid_cat)

    ## cluster the reviews into different categories
    with open(reviews_filename,'r') as fp:
        print ("Clustering Reviews!")
        reader = csv.reader(fp,delimiter="\t")
        count = 0
        for row in reader:
            count += 1
            if count % 1000 == 0:
                print count
            review_id = row[0]
            business_id = row[1]
            review_text = row[2]
            ## note: some business might be deleted! need to check if bid
            ## is in the businessid_cate dictionary
            if business_id in businessid_cate:
                for cat in businessid_cate[business_id]:
                    category_file[cat].write(review_id)
                    category_file[cat].write('\t')
                    category_file[cat].write(review_text)
                    category_file[cat].write('\n')


if __name__ == '__main__':
    #cnx = connect()
    main()
