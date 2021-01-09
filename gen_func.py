

data_in = [[],[]]
data_out = [[],[]]

import math
import numpy as np
# !!! softmax, one category, one node (hence output should be
# like class 0 -> [1,0], class 1 -> [0,1]
for k in np.arange(1, 10, 0.1):
    for b in np.arange(1, 10, 0.1):
        # !!! generate index = 0 with probability 0.7
        if np.random.uniform(0, 1) >= 0.7:
            index = 1
        else:
            index = 0
        data_in[index].append([k**n/b**(n+1) for n in range(10)])
        data_out[index].append([k,b])

# 1/(kx-b) -> c/(kx-b)

# 1/(k-x) -> 1/(1-2x+x^2)
# -> construct linear recurrence and take the coeff as output

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers,regularizers,optimizers
from tensorflow.keras.models import Model


input = keras.Input(shape=(10,))

temp = layers.Dense(512, activation = 'relu', kernel_initializer = 'normal')(input)
temp = layers.Dense(64, activation = 'relu', kernel_initializer = 'normal')(temp)

output = layers.Dense(2, activation='linear', kernel_initializer = 'normal')(temp)

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

axes = plt.gca()
axes.set_ylim([0,1])
plt.plot(history.history['mean_absolute_error'])
plt.plot(list(range(0,max_epoch,5)), history.history['val_mean_absolute_error'])
plt.title('model accuracy')


plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

