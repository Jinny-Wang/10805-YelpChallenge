import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helpers
import math
from text_cnn import TextCNN
from tensorflow.contrib import learn

positive_data_file = "/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/CNN/cnn-text-classification-tf-master/data_yelp/useful_full.pos"
negative_data_file = "/Users/jinny/Desktop/yelp challenge/10805-YelpChallenge/CNN/cnn-text-classification-tf-master/data_yelp/notuseful_full.neg"
x_text, y = data_helpers.load_data_and_labels(positive_data_file, negative_data_file)
