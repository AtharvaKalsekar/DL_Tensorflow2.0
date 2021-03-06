# -*- coding: utf-8 -*-
"""autoregressive_model_time_series.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e8f9b83VkirD205W_AToWUuQvy6SbHKs
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x
import tensorflow as tf
tf.__version__

from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

import numpy as np
import matplotlib.pyplot as plt

series = np.sin(0.1*np.arange(200)) + np.random.randn(200)*0.1

plt.plot(series)
plt.show()

T=10
X=[]
Y=[]

for t in range(len(series)-T):
  x = series[t:t+T]
  X.append(x)
  y = series[t+T]
  Y.append(y)

X=np.array(X).reshape(-1,T)
Y=np.array(Y)
N=len(X)
print('X.shape',X.shape,'Y.shape',Y.shape)

i = Input(shape=(T,))
x = Dense(1)(i)

model = Model(i,x)
model.compile(loss='mae', optimizer=Adam(0.01))

r = model.fit(X[:-N//2],Y[:-N//2], epochs=20, validation_data = (X[-N//2:],Y[-N//2:]))

plt.plot(r.history['loss'],label='loss')
plt.plot(r.history['val_loss'],label='val_loss')
plt.legend()

#wrong forecasting
validation_target = Y[-N//2:]
validation_pred = []

i=-N//2

while len(validation_pred)<len(validation_target):
  p = model.predict(X[i].reshape(1,-1))[0,0]
  i+=1
  validation_pred.append(p)

plt.plot(validation_target, label='target')
plt.plot(validation_pred, label='pred')
plt.legend()

#correct forecasting
validation_target = Y[-N//2:]
validation_pred = []

last_x = X[-N//2]

while len(validation_pred)<len(validation_target):
  p = model.predict(last_x.reshape(1,-1))[0,0]
  validation_pred.append(p)
  last_x = np.roll(last_x,-1)
  last_x[-1] = p

plt.plot(validation_target, label='target')
plt.plot(validation_pred, label='pred')
plt.legend()