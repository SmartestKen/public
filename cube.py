# https://github.com/forestagostinelli/DeepCubeA
# http://deepcube.igb.uci.edu/static/files/SolvingTheRubiksCubeWithDeepReinforcementLearningAndSearch_Final.pdf
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
# use for scramble
import random
# use for open set in A*
import heapq
# use to check if file exists
import os
# for frozen network copy
import copy


class Node():
    def __init__(self, state):
        self.state = state
        self.string = ''.join(str(item) for face in state for item in face)


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.l1 = nn.Linear(144, 5000)
        self.l2 = nn.BatchNorm1d(5000)
        self.l3 = nn.Linear(5000, 1000)
        self.l4 = nn.BatchNorm1d(1000)
        self.l5 = nn.Linear(1000, 1)

        self.blocks = nn.ModuleList()
        for i in range(4):
            # resnet block layers
            self.blocks.append(nn.ModuleList([
                nn.Linear(1000, 1000),
                nn.BatchNorm1d(1000),
                nn.Linear(1000, 1000),
                nn.BatchNorm1d(1000)]))
    def forward(self, x):
        x = F.relu(self.l2(self.l1(x)))
        x = F.relu(self.l4(self.l3(x)))
        for i in range(4):
            initial_x = x
            x = F.relu(self.blocks[i][1](self.blocks[i][0](x)))
            # resnet operation
            x = F.relu(initial_x + self.blocks[i][3](self.blocks[i][2](x)))
        return self.l5(x)


def step(state, action):
    # L clockwise Li counter_clockwise

    if (action == 'L'):
        ini = [32, 33, 34, 35, 36, 37, 38, 39, 8, 15, 14, 0, 7, 6, 24, 31, 30, 16, 23, 22]
        repl = [38, 39, 32, 33, 34, 35, 36, 37, 16, 23, 22, 8, 15, 14, 0, 7, 6, 24, 31, 30]
    elif (action == 'Li'):
        ini = [32, 33, 34, 35, 36, 37, 38, 39, 8, 15, 14, 0, 7, 6, 24, 31, 30, 16, 23, 22]
        repl = [34, 35, 36, 37, 38, 39, 32, 33, 0, 7, 6, 24, 31, 30, 16, 23, 22, 8, 15, 14]
    elif (action == 'R'):
        ini = [40, 41, 42, 43, 44, 45, 46, 47, 12, 11, 10, 20, 19, 18, 28, 27, 26, 4, 3, 2]
        repl = [46, 47, 40, 41, 42, 43, 44, 45, 4, 3, 2, 12, 11, 10, 20, 19, 18, 28, 27, 26]
    elif (action == 'Ri'):
        ini = [40, 41, 42, 43, 44, 45, 46, 47, 12, 11, 10, 20, 19, 18, 28, 27, 26, 4, 3, 2]
        repl = [42, 43, 44, 45, 46, 47, 40, 41, 20, 19, 18, 28, 27, 26, 4, 3, 2, 12, 11, 10]
    elif (action == 'U'):
        ini = [8, 9, 10, 11, 12, 13, 14, 15, 22, 21, 20, 42, 41, 40, 2, 1, 0, 34, 33, 32]
        repl = [14, 15, 8, 9, 10, 11, 12, 13, 34, 33, 32, 22, 21, 20, 42, 41, 40, 2, 1, 0]
    elif (action == 'Ui'):
        ini = [8, 9, 10, 11, 12, 13, 14, 15, 22, 21, 20, 42, 41, 40, 2, 1, 0, 34, 33, 32]
        repl = [10, 11, 12, 13, 14, 15, 8, 9, 42, 41, 40, 2, 1, 0, 34, 33, 32, 22, 21, 20]
    elif (action == 'D'):
        ini = [24, 25, 26, 27, 28, 29, 30, 31, 6, 5, 4, 46, 45, 44, 18, 17, 16, 38, 37, 36]
        repl = [30, 31, 24, 25, 26, 27, 28, 29, 38, 37, 36, 6, 5, 4, 46, 45, 44, 18, 17, 16]
    elif (action == 'Di'):
        ini = [24, 25, 26, 27, 28, 29, 30, 31, 6, 5, 4, 46, 45, 44, 18, 17, 16, 38, 37, 36]
        repl = [26, 27, 28, 29, 30, 31, 24, 25, 46, 45, 44, 18, 17, 16, 38, 37, 36, 6, 5, 4]
    elif (action == 'F'):
        ini = [0, 1, 2, 3, 4, 5, 6, 7, 14, 13, 12, 40, 47, 46, 26, 25, 24, 36, 35, 34]
        repl = [6, 7, 0, 1, 2, 3, 4, 5, 36, 35, 34, 14, 13, 12, 40, 47, 46, 26, 25, 24]
    elif (action == 'Fi'):
        ini = [0, 1, 2, 3, 4, 5, 6, 7, 14, 13, 12, 40, 47, 46, 26, 25, 24, 36, 35, 34]
        repl = [2, 3, 4, 5, 6, 7, 0, 1, 40, 47, 46, 26, 25, 24, 36, 35, 34, 14, 13, 12]
    elif (action == 'B'):
        ini = [16, 17, 18, 19, 20, 21, 22, 23, 30, 29, 28, 44, 43, 42, 10, 9, 8, 32, 39, 38]
        repl = [22, 23, 16, 17, 18, 19, 20, 21, 32, 39, 38, 30, 29, 28, 44, 43, 42, 10, 9, 8]
    elif (action == 'Bi'):
        ini = [16, 17, 18, 19, 20, 21, 22, 23, 30, 29, 28, 44, 43, 42, 10, 9, 8, 32, 39, 38]
        repl = [18, 19, 20, 21, 22, 23, 16, 17, 44, 43, 42, 10, 9, 8, 32, 39, 38, 30, 29, 28]
    else:
        print("bad action")
        return None
    # shallow copy is enough as the color of faces never mutate
    # shallow copy, two sets of reference to the same set of faces
    new_state = [char for char in state]

    for i in range(len(ini)):
        new_state[ini[i]*3:ini[i]*3+3] = state[repl[i]*3:repl[i]*3+3]
    return ''.join(new_state)






# batch the min(...V(s')) term, tensor the V(s) term
# use extend([[x] for i in range])
goal_state = '000' * 8 + '001' * 8 + '010' * 8 + '011' * 8 + '100' * 8 + '101' * 8
actions = ['L', 'Li', 'R', 'Ri', 'U', 'Ui', 'D', 'Di', 'F', 'Fi', 'B', 'Bi']
vnet = Net()
criterion = nn.MSELoss()
optimizer = optim.Adam(vnet.parameters(), lr=0.01)
if os.path.exists("/home/k5shao/Downloads/check_pt"):
    check_pt = torch.load("/home/k5shao/Downloads/check_pt")
    tensor = check_pt['tensor_representations']
    scramble_length = check_pt['scramble_length']
    vnet.load_state_dict(check_pt['vnet_dict'])
    optimizer.load_state_dict(check_pt['optim_dict'])
else:
    tensor = dict()
    scramble_length = 1
vnet.train()



target_v = dict()
target_v[goal_state] = 0
h = dict()
h[goal_state] = 0
vnet2 = copy.deepcopy(vnet)
vnet2.eval()
# beginning of training
while True:
    # 100 per batch?
    for i in range(100):
        # string immutable, assignment equivalent to copy
        start_state = goal_state
        for i in range(scramble_length):
            start_state = step(start_state, random.choice(actions))


        # while not reaching target:
        # pop min f from open set
        # update its child into open set if its current f > g+1+h(child)

        g = dict()
        # action_to_here = dict()
        open = []
        path = []

        # tensor will persist throughout training, h will persist till frozen network is
        # updated, g will only persist per A*
        if tensor.get(start_state,None) == None:
            tensor[start_state] = torch.tensor([float(char) for char in start_state])
        if h.get(start_state, None) == None:
            h[start_state] = vnet2(torch.stack([tensor[start_state]])).data.tolist()[0][0]

        g[start_state] = 0
        # g = 0 so don't bother adding it
        heapq.heappush(open, (h[start_state], start_state))
        # print("h_value:", h[start_state])

        while len(open) != 0:
            # first index is the string state, second index is the f value (ignore)
            temp = heapq.heappop(open)
            cur_state = temp[1]

            if cur_state == goal_state:
                print("ending f value: ", temp[0])
                '''
                while cur_state != start_state:
                    cur_action = action_to_here[cur_state]
                    path = [cur_action] + path
                    # reverse the action to derive path
                    if len(cur_action) == 1:
                        cur_state = step(cur_state, cur_action+'i')
                    else:
                        cur_state = step(cur_state, cur_action[0])
                '''
                break


            for action in actions:
                child = step(cur_state, action)

                if g.get(child, None) == None or (g[child] > (g[cur_state] + 1)):
                    g[child] = g[cur_state] + 1
                    if tensor.get(child, None) == None:
                        tensor[child] = torch.tensor([float(char) for char in child])
                    if h.get(child, None) == None:
                        h[child] = vnet2(torch.stack([tensor[child]])).data.tolist()[0][0]
                    heapq.heappush(open, (g[child] + h[child], child))
                    # print("child: ", g[child], g[child] + h[child])
                    # action_to_here[child] = action

                    # learning rate set to 1
                    temp = target_v.get(cur_state, None)
                    if temp == None or (temp > 1+h[child]):
                        target_v[cur_state] = 1+h[child]





    optimizer.zero_grad()
    # 12 actions only, so ok to compute min
    state_batch, value_batch = zip(*target_v.items())
    state_batch = list(state_batch)

    # convert representation
    for i in range(len(state_batch)):
        state_batch[i] = tensor[state_batch[i]]


    loss = criterion(vnet(torch.stack(state_batch))[:,0], torch.tensor(value_batch))
    # compute gradient
    loss.backward()
    # update using the gradient
    optimizer.step()

    print("loss: ",loss.item())
    # update network and increase scramble length when err small enough
    if loss.item() < 0.05:
        target_v = dict()
        target_v[goal_state] = 0
        h = dict()
        h[goal_state] = 0
        vnet2 = copy.deepcopy(vnet)
        vnet2.eval()
        scramble_length = scramble_length+1
        torch.save({
            'scramble_length': scramble_length,
            'vnet_dict': vnet.state_dict(),
            'optim_dict': optimizer.state_dict(),
            'tensor_representations': tensor
        }, "/home/k5shao/Downloads/checkpt")
