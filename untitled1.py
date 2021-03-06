# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tAWU3Vd0Wy6V4ftC67Yte44lQALYo05a
"""

import pandas as pd
import numpy as np
from tensorflow.keras.optimizers import RMSprop,Adam
from tensorflow.keras.layers import Dense, Flatten,BatchNormalization, Dropout, Lambda, Conv2D, MaxPool2D
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout , LeakyReLU
from sklearn.metrics import classification_report,confusion_matrix
import random


df_train = pd.read_csv('train.csv')
df_test = pd.read_csv('test.csv')



y_train=df_train['label'].values
y_test=df_test['label'].values


df_train.drop('label', axis=1, inplace=True)
df_test.drop('label', axis=1, inplace=True)

x_train = df_train.values
x_test = df_test.values

print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)
# Label Encoding

from keras.utils.np_utils import to_categorical
NumberofClass = 30
y_train = to_categorical(y_train, num_classes = NumberofClass)
y_test = to_categorical(y_test, num_classes = NumberofClass)



x_train=x_train/255
x_test=x_test/255

x_train=np.array(x_train.reshape(-1,28,28,1))
x_test=np.array(x_test.reshape(-1,28,28,1))

batch_size = 128
num_classes = 30
epochs = 50

model = Sequential()

model.add(Conv2D(filters = 128, kernel_size = (4,4), padding = "Same", activation = "relu", input_shape = (28,28,1)))
model.add(MaxPool2D(pool_size = (2,2)))

model.add(Conv2D(filters = 64, kernel_size = (4,4), padding = "Same", activation = "relu"))
model.add(MaxPool2D(pool_size = (2,2)))

model.add(Conv2D(filters = 32, kernel_size = (4,4), padding = "Same", activation = "relu"))
model.add(MaxPool2D(pool_size = (2,2)))

model.add(Conv2D(filters = 16, kernel_size = (4,4), padding = "Same", activation = "relu"))
model.add(MaxPool2D(pool_size = (2,2)))


model.add(Flatten())
model.add(Dense(units = 512, activation = "relu"))
model.add(Dropout(0.5))

model.add(Dense(units = num_classes, activation = "softmax"))
model.compile(optimizer = "rmsprop", loss = "categorical_crossentropy", metrics = ["accuracy"])
model.summary()



print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)


datagen = ImageDataGenerator(
 featurewise_center=False, # set input mean to 0 over the dataset
 samplewise_center=False, # set each sample mean to 0
 featurewise_std_normalization=False, # divide inputs by std of the dataset
 samplewise_std_normalization=False, # divide each input by its std
 zca_whitening=False, # dimesion reduction
 rotation_range=5, # randomly rotate images in the range 5 degrees
 zoom_range = 0.1, # Randomly zoom image 10% 0,1 best
 width_shift_range=0.1, # randomly shift images horizontally 10% +++
 height_shift_range=0.1, # randomly shift images vertically 10%
 horizontal_flip=False, # randomly flip images
 vertical_flip=False) # randomly flip images
datagen.fit(x_train)

filepath="Sign_language_detection.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor= 'val_accuracy' , verbose=2,
save_best_only= True, mode='max',patience=3)
callbacks_list = [checkpoint]

# Fit the model
history = model.fit_generator(datagen.flow(x_train,y_train, batch_size=batch_size), epochs = epochs, validation_data = (x_test,y_test), steps_per_epoch=x_train.shape[ 0] // batch_size , callbacks=callbacks_list)
#Save the model
model.save('sign_language.h5' )

import cv2
from keras.preprocessing.image import img_to_array
alphabet=['A','B','C','D','E','F','G','H','I','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y']
def classify(image):
 image = cv2.resize(image, (28, 28))
 image = image.astype("float") / 255.0
 image = img_to_array(image)
 image = np.expand_dims(image, axis=0)
 proba=model.predict(image)
 idx = np.argmax(proba)
 return alphabet[idx]

classify(x_train[3]*255)

