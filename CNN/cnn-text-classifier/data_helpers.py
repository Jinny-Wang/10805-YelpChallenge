## 2017-12-01 : add load_embedding_vectors_word2vec

import numpy as np
import re
import itertools
from collections import Counter
import sys

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels(positive_data_file, negative_data_file):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """

    # Load data from files
    positive_examples = list(open(positive_data_file, encoding="utf-8").readlines())
    positive_examples = [s.strip() for s in positive_examples]
    negative_examples = list(open(negative_data_file,encoding="utf-8").readlines())
    negative_examples = [s.strip() for s in negative_examples]
    # Split by words
    x_text = positive_examples + negative_examples
    #x_text = [clean_str(sent) for sent in x_text]
    # Generate labels
    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]
    y = np.concatenate([positive_labels, negative_labels], 0)
    return [x_text, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]

## load shuffled train and test data point
## return [x_train,y_train] , [x_test,y_test]
def load_shuffled_data_labels(trainFile,testFile):
    
### load embedding vectors given word vector file
## vocabulary : dictionary returned from tensorflow learn.preprocessing.VocabularyProcessor(max_document_length)
#               This is decided by the training data.
## filename : path to the word vector file
## isBinary : True indicates that the wordvector file is in binary format
#             False indicates that the wordvector file is in text format
def load_embedding_vectors_word2vec(vocabulary,filename,isBinary):
    encoding = 'utf-8'
    with open(filename,'rb') as f:
         header  = f.readline()
         vocab_size, vector_size = map(int,header.split()) #vocab_size  : vocab_size in word2vec

         #initial matrix with random uniform
         embedding_vectors = np.random.uniform(-0.25,0.25,(len(vocabulary),vector_size))
         if isBinary:
             binary_len = np.dtype('float32').itemsize * vector_size  ## item size : length of a single element in the array in byte s
             for line_no in range(vocab_size):
                 word = []
                 while True:
                     ch = f.read(1)
                     if ch == b' ':
                         break
                     if ch == b'':
                         raise EOFError("unexpected end of input; is count incorrect or file otherwise damaged?")
                     if ch != b'\n':
                        word.append(ch)
                     # print (binascii.b2a_uu(ch))
                 # print (word)
                 word = str(b''.join(word),encoding=encoding,errors='strict')
                 # print ("word",word)
                 idx = vocabulary.get(word)
                 if idx and idx !=0 : ## if the word in pretrained word vector is in the custom vocabulary
                     embedding_vectors[idx] = np.fromstring(f.read(binary_len),dtype='float32')
                     #print (embedding_vectors[idx])
                 else:  ## if the word is not in our costom vocabulary-> skip the current word vector
                     f.seek(binary_len,1)
                     #print ("else")
         else:
            for line_no in range(vocab_size):
                line = f.readline()
                if line == b'':
                    raise EOFError("unexpected end of input; is count incorrect or file otherwise damaged?")
                parts = str(line.strip(),encoding=encoding, errors='strict').split(" ")
                if len(parts) != vector_size + 1:
                    raise ValueError("invalid vector on line %d ((is this really the text format?))" % (line_no))
                word,vector = parts[0],list(map('float32',parts[1:]))
                idx = vocabulary.get(word)
                if idx and idx != 0:
                    embedding_vectors[idx] = vector
         f.close()
         return embedding_vectors
