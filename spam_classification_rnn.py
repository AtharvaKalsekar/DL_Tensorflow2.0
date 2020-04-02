# -*- coding: utf-8 -*-
"""spam_classification_RNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dAqRMPINIPznxee__k9fc0g_WiC0z636
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x
import tensorflow as tf
tf.__version__

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Dense, GlobalMaxPooling1D, LSTM, Embedding
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split

!wget https://lazyprogrammer.me/course_files/spam.csv

df = pd.read_csv('spam.csv', encoding='ISO-8859-1')

df.head()

df = df.drop(['Unnamed: 2','Unnamed: 3','Unnamed: 4'],axis=1)

df.columns = ['labels','data']

df.head()

df['b_labels'] = df['labels'].map({'ham':0,'spam':1})
Y = df['b_labels'].values

df_train, df_test, Y_train, Y_test = train_test_split(df['data'], Y, test_size=0.33)

MAX_VOCAB_SIZE = 20000
tokenizer = Tokenizer(num_words= MAX_VOCAB_SIZE)
tokenizer.fit_on_texts(df_train)
sequences_train = tokenizer.texts_to_sequences(df_train)
sequences_test = tokenizer.texts_to_sequences(df_test)

word2idx = tokenizer.word_index
V = len(word2idx)
print("number of unique words = ",V)

data_train = pad_sequences(sequences_train)
print("data_train.shape = ",data_train.shape)
T = data_train.shape[1]

data_test = pad_sequences(sequences_test, maxlen=T)
print("data_test.shape = ",data_test.shape)

D = 20
M = 15
i = Input(shape=(T,))
x = Embedding(V+1,D)(i)
x = LSTM(M, return_sequences=True)(x)
x = GlobalMaxPooling1D()(x)
x = Dense(1, activation='sigmoid')(x)
model = Model(i,x)

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

r = model.fit(data_train,Y_train, epochs = 10, validation_data=(data_test,Y_test))

plt.plot(r.history['loss'],label='loss')
plt.plot(r.history['val_loss'],label='val_loss')
plt.legend()

plt.plot(r.history['accuracy'],label='accuracy')
plt.plot(r.history['val_accuracy'],label='val_accuracy')
plt.legend()