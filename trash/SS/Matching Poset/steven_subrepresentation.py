#from __future__ import print_function
import itertools


def getPsi(lda, alpha):

    # pre-check (lda and alpha are both partition of n)
    if sum(lda) != sum(alpha):
        print("bad partition")
        return -1

    psi = 0
    queue = [[lda, alpha, 0]]
    while len(queue) != 0:
        arg = queue.pop(0)
        if len(arg[1]) == 0:
            if len(arg[0]) == 0:
                psi += (-1)**arg[2]
                #print("end " + str(arg[2]))
            else:
                print("error in getSubDiagram")
                break
        else:
            queue = queue + getSubDiagrams(arg[0],arg[1],arg[2])
    #print("psi=" + str(psi))
    return psi




# diagram comes from lda, height is the current strip height
def getSubDiagrams(lda, alpha, height):
    #print("---------------------------")
    #print(lda)
    # collect border
    border = []
    max_width_index = lda[0]-1
    max_height_index = len(lda)-1

    # row, col
    currentPt = (0, max_width_index)
    bdEnd = (max_height_index, 0)
    while currentPt != bdEnd:
        #print(currentPt)
        border.append(currentPt)
        if (currentPt[0] < max_height_index) and (currentPt[1] <= lda[currentPt[0]+1]-1):
            currentPt = (currentPt[0]+1, currentPt[1])
        elif currentPt[1] > 0:
            currentPt = (currentPt[0], currentPt[1]-1)
        else:
            print("error")
            break
    border.append(bdEnd)

    # start point index in border
    start = [0]
    for i in range(1, len(border)):
        if border[i][0]-1 == border[i-1][0]:
            start.append(i)
    #print(border)
    #print(start)
    # check against length, (current alpha[0])
    subDiagrams = []
    length = alpha[0]
    #print(length)
    for pt_index in start:
        # out of index bound
        if (pt_index+length-1) > (len(border) - 1):
            continue
        # exactly at the end of border, good
        elif (pt_index+length-1) == (len(border) - 1):

            subLda = list(lda)
            for i in range(pt_index, pt_index+length):
                subLda[border[i][0]]-=1
            while (len(subLda) > 0) and (subLda[-1] == 0):
                subLda.pop(-1)
            subDiagrams.append([subLda, alpha[1:],
                                height+border[pt_index+length-1][0]-border[pt_index][0]])

        # check direction of border at the end of strip to decide strip validity
        else:
            if border[pt_index+length][1] < border[pt_index+length-1][1]:
                subLda = list(lda)
                for i in range(pt_index, pt_index+length):
                    subLda[border[i][0]]-=1
                while (len(subLda) > 0) and (subLda[-1] == 0):
                    subLda.pop(-1)
                subDiagrams.append([subLda, alpha[1:],
                                    height+border[pt_index+length-1][0]-border[pt_index][0]])

    #print(len(subDiagrams))
    return subDiagrams

def applyPermutation(pm, perm):
    temp2 = []
    for number in pm:
        temp2.append(perm[number-1])
    permuted_pm = []
    for i in range(0,7,2):
        if temp2[i] < temp2[i+1]:
            permuted_pm.append([temp2[i], temp2[i+1]])
        else:
            permuted_pm.append([temp2[i+1], temp2[i]])
    permuted_pm = sorted(permuted_pm)
    newPm = []
    for connection in permuted_pm:
        newPm += connection
    return newPm

def pmToStr(pm):
    return ''.join(str(num) for num in pm)

def generatePmList(size):
    pmListTemp = list(itertools.permutations(list(range(1,size+1))))
    pmList = []
    invalidFlag = 0
    for pm in pmListTemp:
        if pm[0] != 1:
            continue

        for i in range(0,size-3,2):
            if pm[i] >= pm[i+2]:
                invalidFlag = 1
        if invalidFlag == 1:
            invalidFlag = 0
            continue

        for i in range(0,size-1,2):
            if pm[i] >= pm[i+1]:
                invalidFlag = 1
        if invalidFlag == 1:
            invalidFlag = 0
            continue



        # a valid pm
        pmList.append(pm)
    pmList.sort()
    return pmList


def generatePmDict(pmList):
    pmDict = {}
    for index,pm in enumerate(pmList):
        pmDict[pmToStr(pm)] = index
    return pmDict

'''
ldaList = Partitions(4).list()
permList = list(itertools.permutations(list(range(1,9))))
pmList = generatePmList(8)
pmDictionary = generatePmDict(pmList)


w,h = 105,105

for lda in ldaList:
    print('start' + str(lda))
    matrix = [[0 for x in range(w)] for y in range(h)]
    lda = [i * 2 for i in lda]
    for perm in permList:
        #print('start ' + str(perm))
        permObj = Permutation(list(perm))

        permMat = [[0 for x in range(w)] for y in range(h)]
        test1 = list(range(105))
        test2 = list(range(105))
        for pm in pmList:
            newPm = applyPermutation(pm, perm)
            #print(pmDictionary[pmToStr(newPm)],pmDictionary[pmToStr(pm)])
            test1.remove(pmDictionary[pmToStr(newPm)])
            test2.remove(pmDictionary[pmToStr(pm)])
            permMat[pmDictionary[pmToStr(newPm)]][pmDictionary[pmToStr(pm)]] = 1
        if (len(test1) > 0) or (len(test2) > 0):
            print('error')



        #print('getpsi')


        alpha = permObj.cycle_type()
        # print str(alpha)+" "+str(lda)
        psi = getPsi(lda,alpha)

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = matrix[i][j] + psi*permMat[i][j]

        #print('end' + str(perm))



    print('end ' + str(lda))

    strmatrix = ''
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            strmatrix += ' ' + str(matrix[i][j])
        strmatrix += ';\n'
    with open('subrepresentation'+str(lda)+'.txt', 'w') as f:
        print(strmatrix, file=f)
'''
getPsi(list(range(30, 0, -1)), list(range(30, 0, -1)))