with open(r'/home/k5shao/Desktop/Steven Sam/8_point_graph.txt', 'r') as f:
    contents = f.readlines()
childList = [None]*106
for line in contents:
    info = line.split()
    parent = int(info[0])
    if childList[parent] == None:
        childList[parent] = set()
    childList[parent].add(int(info[1]))
for i in range(105, -1, -1):
    if childList[i] != None:
        for child in childList[i]:
            if childList[child] != None:
                childList[i] = childList[i].difference(childList[child])

for i in range(106):
    if childList[i] != None:
        print(i, childList[i])