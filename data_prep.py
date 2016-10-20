import numpy
import string
import nltk
import itertools
from nltk.tokenize import sent_tokenize
import cPickle as pickle
import re


vocabulary_size = 8000
unknown_token = "UNKNOWN_TOKEN"
sentence_start_token = "SENTENCE_START"
sentence_end_token = "SENTENCE_END"
 
tokenized_sentences = pickle.load(open("../data/in_soviet_russia.p", "rb"))
tokenized_sentences = tokenized_sentences + pickle.load(open("../data/in_soviet_russia2.p","rb"))

#### insert code here to clean the dataset (get rid of multiple !, weird punctuation and caps lock and other crap)
tokenized_sentences = [i.lower() for i in tokenized_sentences]
tokenized_sentences = [re.sub("\s\s+" , " ", i) for i in tokenized_sentences]  

tokenized_sentences = [sentence_start_token + " " + x + " " +  sentence_end_token for x in tokenized_sentences]
print "Parsed %d sentences." % (len(tokenized_sentences))

# Count the word frequencies
words = []
for i in tokenized_sentences:
	words+=i.split(" ")
word_freq = nltk.FreqDist(words)
print "Found %d unique words tokens." % len(word_freq.items())

 
# Get the most common words and build index_to_word and word_to_index vectors
vocab = word_freq.most_common(vocabulary_size-1)
index_to_word = [x[0] for x in vocab]
index_to_word.append(unknown_token)
word_to_index = dict([(w,i) for i,w in enumerate(index_to_word)])

print "Using vocabulary size %d." % vocabulary_size
print "The least frequent word in our vocabulary is '%s' and appeared %d times." % (vocab[-1][0], vocab[-1][1])

# Replace all words not in our vocabulary with the unknown token
for i, sent in enumerate(tokenized_sentences):
    tokenized_sentences[i] = [w if w in word_to_index else unknown_token for w in sent.split(" ")]



print "\nExample sentence: '%s'" % tokenized_sentences[0]
print "\nExample sentence after Pre-processing: '%s'" % tokenized_sentences[0]
 
# Create the training data
X_train = numpy.asarray([[word_to_index[w] for w in sent[:-1]] for sent in tokenized_sentences])
y_train = numpy.asarray([[word_to_index[w] for w in sent[1:]] for sent in tokenized_sentences])


pickle.dump(tokenized_sentences,open("tokenized_sentences","wb"))
pickle.dump(word_to_index,open("word_to_index","wb"))
pickle.dump(index_to_word,open("index_to_word","wb"))
numpy.save("insoviet_x",X_train)
numpy.save("insoviet_y",y_train)




