import gensim
import logging
import os
from gensim.models import Word2Vec
import numpy as np
import sys
# positive_data_file = "./data_yelp/useful.pos"
# negative_data_file = "./data_yelp/notuseful.neg"
#
# sentences = [['first','sentence'],['second','sentence']]
#
# vocabulary = {'first':1,'second':2,'haha':3}

dirname = ["./data_yelp/useful.pos","./data_yelp/notuseful.neg"]

class MySentences(object):
    def __init__(self,dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in dirname:
            for line in open(fname):
                yield line.split()




# min_count: lowest number of occurence tobe considered , default is 5
# size : size of the nn layer. bigger -> larger training data
# workers: for parallizing the training process

sentences = MySentences(dirname)
# for line in sentences:
#     print (line)


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
print ("Start Training..")
model = Word2Vec(sentences,min_count=100,size=64,workers=4)
# # print (model)
# # print (model['first'])
# model.save('./mymodel')
print ("Finished Training word2vec..")
print ("Saving Models")
model.wv.save_word2vec_format('./yelp_sampled_reviews_word2vec.bin', binary=True)
print ("Model saved.")
