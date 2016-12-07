
from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy
import cPickle as pickle
import random
import sys


#loading data
a = pickle.load(open("../data/one_does_not_simply.p",'rb'))
text = ""
for i in a:
    text=text+" "+i


text = text.lower()
print('corpus length:', len(text))

chars = sorted(list(set(text)))
print('total chars:', len(chars))


'''
Temporary fix for removing stupid useless characters

'''

permitted = chars[37:63]
permitted.append(chars[0])
not_permitted = []

for i in chars:
    if not i in permitted:
        not_permitted.append(i)


for i in not_permitted:
    text = text.replace(i,"")


chars = sorted(list(set(text)))
print('total chars:', len(chars))


char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

maxlen = 50
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))


X = numpy.zeros((len(sentences), maxlen, len(chars)), dtype=numpy.bool)
y = numpy.zeros((len(sentences), len(chars)), dtype=numpy.bool)
for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
                X[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1


# build the model: a single LSTM
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars)), return_sequences=True,))
model.add(LSTM(128))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
        preds = numpy.asarray(preds).astype('float64')
        preds = numpy.log(preds) / temperature
        exp_preds = numpy.exp(preds)
        preds = exp_preds / numpy.sum(exp_preds)
        probas = numpy.random.multinomial(1, preds, 1)
        return numpy.argmax(probas)

sentence = text[102:119]



for iteration in range(1, 20):
    with open('generated_2','ab') as f:
        f.write('\n')
        f.write('-------------------------------------------')
        f.write('Iteration'+str(iteration))
    print('\n')
    print('-------------------------------------------')
    print('Iteration'+str(iteration))
    model.fit(X, y, batch_size=4492, nb_epoch=1)
    generated = ''

    for i in range(100):
        x = numpy.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x[0, t, char_indices[char]] = 1.

        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char
    with open('generated','ab') as f:
        f.write(str(generated)+'\n')
    print(str(generated)+'\n')
f.close()
