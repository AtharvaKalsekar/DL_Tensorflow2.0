# -*- coding: utf-8 -*-
"""cnn_cifar10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f5IXQXOH15j-IMOCbKl_20S3i53bQC0E
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x
import tensorflow as tf
tf.__version__

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout
from tensorflow.keras.models import Model

cifar10 = tf.keras.datasets.cifar10

(x_train,y_train), (x_test,y_test) = cifar10.load_data()
x_train = x_train/255
x_test = x_test/255
y_train = y_train.flatten()
y_test = y_test.flatten()

print("x_train.shape = ",x_train.shape)
print("y_train.shape = ",y_train.shape)

K = len(set(y_train))
print("numbr of classes = ",K)

i = Input(shape=x_train[0].shape)
x = Conv2D(filters=32, kernel_size=(3,3), strides=2, activation='relu')(i)
x = Conv2D(filters=64, kernel_size=(3,3), strides=2, activation='relu')(x)
x = Conv2D(filters=128, kernel_size=(3,3), strides=2, activation='relu')(x)
x = Flatten()(x)
x = Dropout(0.2)(x)
x = Dense(512,activation='relu')(x)
x = Dense(K, activation='softmax')(x)

model = Model(i,x)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
r = model.fit(x_train,y_train, validation_data=(x_test,y_test), epochs=15)

plt.plot(r.history['loss'],label='loss')
plt.plot(r.history['val_loss'], label='val_loss')
plt.legend()

plt.plot(r.history['accuracy'],label='acc')
plt.plot(r.history['val_accuracy'], label='val_acc')
plt.legend()