####Convert word combination tokens to bag of words representation####
#Command line input: csv file of data to be processed


import sys
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re



def tokenize(text):
    return(re.split('\t',text.strip()))

corpus = []
count = 0
for line in sys.stdin:
  corpus.append(line)
  # count += 1
  # if count == 10:
  #   break

print("Done reading corpus")
print("Vectorizing")
vectorizer = CountVectorizer(tokenizer=tokenize)
bog = vectorizer.fit_transform(corpus).toarray()
print("Saving bow representation")
outfile = 'bow_dist2'
np.save(outfile,bog)

#print(len(bog[0]))