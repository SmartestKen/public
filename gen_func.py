



# 1. generate LR through lr calculator, upload to google drive
# 2. neural code
# input: 2 src , 1 target partition
# output: whether it is zero

def get_partitions(max):

    partitions = [[] for i in range(max+1)]
    for n in range(1,max+1):
        # compute partition with sum = n
        # an obvious one is [n]
        partitions[n] = [(n,)]
        for i in range(1,n):
            for item in partitions[n-i]:
                if item[0] <= i:
                    partitions[n].append(tuple([i] + list(item)))

    return partitions

uv_max = 10
lda_max = 2*uv_max

partitions = [j for sub in get_partitions(uv_max) for j in sub]
input_str = ['' for i in range(lda_max)]
for p1 in partitions:
    for p2 in partitions:
        input_str[sum(p1) + sum(p2) - 1] += ' '.join(map(str, p1)) + ' - ' + ' '.join(map(str, p2)) + '\n'

concated_input = ''
for i in range(lda_max):
    concated_input += input_str[i]

with open('/home/public/LR_in', 'w') as f:
    f.write(concated_input)




with open("/home/public/LR_out") as f:
    content = f.readlines()
# data1 for training, data2 for testing

partitions = get_partitions(lda_max)
for i in range(lda_max+1):
    partitions[i] = set(partitions[i])

data_in = [[],[]]
data_out = [[],[]]
cut = int(len(content)*0.7)
chunk = 0


positive_count = 0
zero_count = 0

uv = []
lda_left = []
change_flag = 0

for i,item in enumerate(content):

    if i > cut:
        chunk = 1

    # splitting line
    if item == '---\n':
        change_flag = 1
        continue

    # normal data line
    temp = item.split(")")
    temp1 = temp[0].split("(")
    temp2 = temp[1].split('-')

    # output label
    part0 = int(temp1[0])

    # _temp used for removal later
    part1_temp = [int(x) for x in temp1[1].split(",")]
    part2_temp = [int(x) for x in temp2[0].split()]
    part3_temp = [int(x) for x in temp2[1].split()]



    # add padding to all input
    part1 = part1_temp + [0] * (lda_max - len(part1_temp))
    part2 = part2_temp + [0] * (lda_max - len(part2_temp))
    part3 = part3_temp + [0] * (lda_max - len(part3_temp))


    if change_flag == 1:
        # not the first chunk
        if len(uv) != 0:
            for item in lda_left:
                data_in[chunk].append(list(item) + [0] * (lda_max - len(item)) + uv[0] + uv[1])
                data_out[chunk].append([0,1])
            # print("hahahah")

        uv = [part2, part3]
        lda_left = partitions[sum(part2_temp) + sum(part3_temp)].copy()
        change_flag = 0

    # use tuple for paritition sources to avoid unexpected changes
    if tuple(part1_temp) not in lda_left:
        print("ERROR lda", part1_temp, part2_temp, part3_temp, lda_left)


    lda_left.remove(tuple(part1_temp))
    data_in[chunk].append(part1 + part2 + part3)
    data_out[chunk].append([1, 0])



    if (len(part1) != lda_max) or (len(part2) != lda_max) or (len(part3) != lda_max):
        print("ERROR")

'''
print(data_in[0][4])
print(data_in[0][7])
print(data_out[0][0:20])

exit(0)
'''
# !!! softmax, one category, one node (hence output should be
# like class 0 -> [1,0], class 1 -> [0,1]



import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers,regularizers,optimizers
import numpy as np


model = keras.Sequential()
model.add(keras.Input(shape=(lda_max*3,)))
model.add(layers.Dense(512, activation='relu', kernel_regularizer= regularizers.l2(0.001)))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.Dense(2, activation='softmax'))

Optim = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=True)

model.compile(optimizer=Optim,loss='categorical_crossentropy', metrics=['acc'])
model.summary()

# data_tfin = tf.convert_to_tensor(np.asarray(data_in[0]), np.float32)
# data_tfout = tf.convert_to_tensor(np.asarray(data_out[0]), np.float32)
# train_dataset = tf.data.Dataset.from_tensor_slices((data_in[0], data_out[0]))
# train_dataset = train_dataset.shuffle(buffer_size=1024)
# print(data_tfin.get_shape().as_list())

# !!! input always of the shape (batch_size, ...),
# whether use (...) or batch_size, ...) for input
# layer depends on framework
model.fit(np.asarray(data_in[0]), np.asarray(data_out[0]), epochs = 1000, verbose = 2,
          validation_data = (np.asarray(data_in[1]), np.asarray(data_out[1])), validation_freq = 5)



