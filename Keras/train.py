from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils

import csv

batch_size = 128
nb_classes = 2
nb_epoch = 20

def load_data():
   x_train=[]
   Y_train=[]
   x_test=[]
   Y_test=[]
   with open('dataset/train.csv','rb') as myFile1:    
      lines1=csv.reader(myFile1)    
      i=0  
      for line in lines1:  
         #对于训练数据删除前三列，其中第二列性别当作标签，0表示男，1表示女	  
         if i > 0:
            del line[0]
            if line[0]=='\xe7\x94\xb7':
               Y_train.append(0)
            else: 
               Y_train.append(1)
            del line[0]
            del line[0]
            x_train.append(line)                   
         i=i+1
   x1=np.array(x_train)
   y1=np.array(Y_train)
   with open('dataset/predict.csv','rb') as myFile2:    
      lines2=csv.reader(myFile2)    
      i=0  
      for line in lines2:        
         if i > 0:
            del line[0]
            if line[0]=='\xe7\x94\xb7':
               Y_test.append(0)
            else: 
               Y_test.append(1)
            del line[0]
            del line[0]
            x_test.append(line)         
         i=i+1
   x2=np.array(x_test)
   y2=np.array(Y_test) 
   return (x1, y1), (x2, y2)   

# the data, shuffled and split between train and test sets
(X_train, y_train), (X_test, y_test) = load_data()

X_train = X_train.reshape(1858, 26)
X_test = X_test.reshape(200, 26)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

#分成3层，中间隐层有512个节点
model = Sequential()
model.add(Dense(512, input_shape=(26,)))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(2))
model.add(Activation('softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

history = model.fit(X_train, Y_train,
                    batch_size=batch_size, nb_epoch=nb_epoch,
                    verbose=1, validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
