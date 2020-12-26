from random import randrange

data_in = [[],[]]
data_out = [[],[]]


# !!! softmax, one category, one node (hence output should be
# like class 0 -> [1,0], class 1 -> [0,1]
for i in range(10000):
    index = 0
    if randrange(10) > 6:
        index = 1
    x = i/10000
    data_in[index].append(x)
    data_out[index].append(1/(1-x))




import numpy as np

from tensorflow import keras
from tensorflow.keras import layers,regularizers,optimizers
from tensorflow.keras.models import Model


x0 = keras.Input(shape=(1,))
x1 = layers.Dense(64, activation='relu', kernel_initializer = 'normal')(x0)
x2 = layers.Dense(16, activation='relu', kernel_initializer = 'normal')(x1)
x3 = layers.Dense(1, activation='linear', kernel_initializer = 'normal')(x2)

model = Model(x0, x3)

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
history = model.fit(np.asarray(data_in[0]), np.asarray(data_out[0]), epochs = 100, verbose = 2,
    validation_data = (np.asarray(data_in[1]), np.asarray(data_out[1])), validation_freq = 5)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

