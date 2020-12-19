import matplotlib.pyplot as plt
with open("/home/public/LR_nn_out") as f:
    content = f.readlines()
content = content[1::2]
content = [x.strip().split() for x in content]
train_loss = []
train_acc = []
val_loss = []
val_acc = []
for tokens in content:
    # print(len(tokens))
    # print(tokens)
    train_loss.append(tokens[5])
    train_acc.append(tokens[8])
    if len(tokens) == 15:
        val_loss.append(tokens[11])
        val_acc.append(tokens[14])

plt.figure()
x_for_train = [x for x in range(1000)]
x_for_val = [5*x for x in range(200)]
plt.plot(x_for_train, train_loss)
plt.plot(x_for_val, val_loss)
plt.xlabel("iteration")
plt.ylabel("loss")

print(train_loss)
print(val_loss)
plt.figure()
plt.plot(x_for_train, train_acc)
plt.plot(x_for_val, val_acc)
plt.xlabel("iteration")
plt.ylabel("accuracy")
plt.show()
