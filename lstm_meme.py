from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as numpy


X_train = np.load("insoviet_x.npy")
y_train = np.load("insoviet_y.npy")

