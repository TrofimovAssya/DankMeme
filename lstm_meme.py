import numpy
import cPickle as pickle
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


#loading data files + dictionaries
tokenized_sentences = pickle.load(open("tokenized_sentences","rb"))
word_to_index = pickle.load(open("word_to_index","rb"))
index_to_word = pickle.load(open("index_to_word","rb"))
X_train = numpy.load("insoviet_x")
y_train = numpy.load("insoviet_y")


model = Sequential()
model.add(LSTM(32, input_dim=64, input_length=10))

