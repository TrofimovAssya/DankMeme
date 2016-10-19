import numpy
import string
import nltk
import itertools
from nltk.tokenize import sent_tokenize
import cPickle as pickle


# load the text (poe)
filename = "../data/modern_ghost_stories.txt"
raw_text = open(filename).read()
raw_text = raw_text.lower()
raw_text = raw_text.replace('\n',' ')
wrap = ['\xa0','\xa2','\xa6','\xa9','\xb3','\xb4','\xb9','\xbc','\xc3']
for i in wrap:
    raw_text = raw_text.replace(i,"")



sentences = sent_tokenize(raw_text)
memes1 = pickle.load(open("../data/in_soviet_russia.p"))
memes2 = pickle.load(open("../data/in_soviet_russia2.p"))
sentences = sentences+memes1+memes2

sentence_start_token = "SENTENCE_START"
sentence_end_token = "SENTENCE_END"

sentences = ["%s %s %s" % (sentence_start_token, x, sentence_end_token) for x in sentences]
print "Parsed %d sentences." % (len(sentences))
tokenized_sentences = [nltk.word_tokenize(sent) for sent in sentences]
word_freq = nltk.FreqDist(itertools.chain(*tokenized_sentences))
print "Found %d unique words tokens." % len(word_freq.items())


vocabulary_size = len(word_freq.items())
word_to_index = dict([(w,i) for i,w in enumerate(word_freq)])
index_to_word = dict([(i,w) for i,w in enumerate(word_freq)])
print "Using vocabulary size %d." % vocabulary_size


X_train = numpy.asarray([[word_to_index[w] for w in sent[:-1]] for sent in tokenized_sentences])
y_train = numpy.asarray([[word_to_index[w] for w in sent[1:]] for sent in tokenized_sentences])

pickle.dump(tokenized_sentences,open("tokenized_sentences","wb"))
pickle.dump(word_to_index,open("word_to_index","wb"))
pickle.dump(index_to_word,open("index_to_word","wb"))
numpy.save("insoviet_x",X_train)
numpy.save("insoviet_y",y_train)




