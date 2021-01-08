from random import randrange

data_in = [[],[]]
data_out = [[],[]]

import math
# !!! softmax, one category, one node (hence output should be
# like class 0 -> [1,0], class 1 -> [0,1]
for k in range(1,100):
    for b in range(1,100):
        # !!! generate index = 0 with probability 0.7
        index = 0
        data_in[index].append([(-1)**n*k**n/b**(n+1) for n in range(1,100)])
        data_out[index].append([k,b])




import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers,regularizers,optimizers
from tensorflow.keras.models import Model


input = keras.Input(shape=(1,))


temp = layers.Dense(512, activation = 'relu', kernel_initializer = 'normal')(input)
temp = layers.ReLU()(temp)

# temp_res = tf.concat(input*64, 0)
temp = layers.Dense(64, activation = 'relu', kernel_initializer = 'normal')(temp)
# temp = layers.Add()([temp, temp_res])
# temp = layers.ReLU()(temp)

output = layers.Dense(1, activation='linear', kernel_initializer = 'normal')(temp)

model = Model(input, output)

Optim = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=True)

model.compile(optimizer=Optim,loss='mean_absolute_error', metrics=['mean_absolute_error'])
model.summary()

# data_tfin = tf.convert_to_tensor(np.asarray(data_in[0]), np.float32)
# data_tfout = tf.convert_to_tensor(np.asarray(data_out[0]), np.float32)
# train_dataset = tf.data.Dataset.from_tensor_slices((data_in[0], data_out[0]))
# train_dataset = train_dataset.shuffle(buffer_size=1024)
# print(data_tfin.get_shape().as_list())

# !!! actual input always of the shape (batch_size, ...),
# but there may be syntax difference across frameworks
max_epoch = 100
history = model.fit(np.asarray(data_in[0]), np.asarray(data_out[0]), epochs = max_epoch, verbose = 2,
    validation_data = (np.asarray(data_in[1]), np.asarray(data_out[1])), validation_freq = 5)

import matplotlib.pyplot as plt
print(history.history.keys())
plt.plot(history.history['mean_absolute_error'])
plt.plot(list(range(0,max_epoch,5)), history.history['val_mean_absolute_error'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

