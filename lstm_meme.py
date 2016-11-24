
from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy
import random
import sys


#loading data
X_train = numpy.load("insoviet_x.npy")
y_train = numpy.load("insoviet_y.npy")

tokenized_sentences = pickle.load(open("tokenized_sentences","wb"))
word_to_index = pickle.load(open("word_to_index","wb"))
index_to_word = pickle.load(open("index_to_word","wb"))

