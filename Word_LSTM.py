import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Embedding
from keras.utils import np_utils
import keras
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
import os
import re
import sys

path = os.path.dirname(os.path.realpath(__file__)) + '/data/lu.txt'
wordarray = []
row_words = open(path, 'r', encoding="utf8").read()
row_words = row_words[:50000]  # 全集大概100万字,只取前5万
n_words = sorted(list(set(row_words)))  # 去重
char_to_int = dict((c, i) for i, c in enumerate(n_words))
int_to_char = dict((i, c) for i, c in enumerate(n_words))
n_vocab = len(n_words)
print('n_vocab-->', n_vocab)

seq_length = 40  # 句子长度
dataX = []
dataY = []
# 处理数据,并保持数据的时间关联性
for i in range(0, len(row_words) - seq_length, 1):
    seq_in = row_words[i:i + seq_length]
    seq_out = row_words[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
dataX = np.reshape(dataX, (len(dataX), seq_length, 1))
dataY = keras.utils.np_utils.to_categorical(dataY)

print(dataX.shape)
print(dataY.shape)

x = np.zeros((len(dataX), seq_length, n_vocab), dtype=np.bool)
for i, sentence in enumerate(dataX):
    for t, char in enumerate(sentence):
        x[i, t, char] = 1
dataX = x

print(dataX.shape)
print(dataY.shape)
model = Sequential()
model.add(LSTM(128, input_shape=(seq_length, n_vocab)))
model.add(Dropout(0.2))
model.add(Dense(n_vocab, activation='softmax'))
model.summary()
filepath = "weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = keras.callbacks.ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model.compile(optimizer='adam', loss='categorical_crossentropy')
# model.fit(dataX, dataY, epochs=50, batch_size=100, callbacks=callbacks_list)
model = keras.models.load_model('weights-improvement-50-2.1862.hdf5')
# 随机取训练数据作为随机种子
start = np.random.randint(0, len(dataX) - 1)
pattern = dataX[start]
pre = []
for i in range(200):  # 生成200字的文本
    (w, h) = pattern.shape
    x = np.reshape(pattern, (1, w, h))
    prediction = model.predict(x, verbose=0)
    index = np.argmax(prediction)
    result = int_to_char[index]
    pre.append(result)
    index_word = np.zeros((1, n_vocab), dtype=np.bool)
    index_word[0][index] = 1
    pattern = np.concatenate((pattern, index_word))
    pattern = pattern[1:len(pattern)]
print(''.join(pre))
