import itertools

def getColumn(matrix, i):
    return [row[i] for row in matrix]


def applyPermutation(pm, perm, size):
    temp2 = []
    for number in pm:
        temp2.append(perm[number-1])
    permuted_pm = []
    for i in range(0,size-1,2):
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

def oddDoubleFactorial(size):
    num = 3
    product = 1
    while (num <= size):
        product *= num
        num += 2
    return product

def factorial(size):
    num = 2
    product = 1
    while (num <= size):
        product *= num
        num += 1
    return product 
    

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
       
# index 1 based
def generateMat(leading_term,size):
    
    
    w, h = factorial(size),oddDoubleFactorial(size)
    matrix = [[0 for x in range(w)] for y in range(h)] 
    
    
    pmList = generatePmList(size)
    pmDict = generatePmDict(pmList)
    coeffList = [0]*oddDoubleFactorial(size)

        
    
    

    for i in range(oddDoubleFactorial(size)):
        if (i+1) < leading_term:
            coeffList[i] = 'a' + str(i+1)
        elif (i+1) == leading_term:
            coeffList[i] = '1'
        else:
            coeffList[i] = '0'




    all_perm_list = list(itertools.permutations(range(1,size+1)))



    for col_index in range(len(all_perm_list)):
        perm = all_perm_list[col_index]
        for i in range(len(pmList)):
        
            pm = pmList[i]
            coeff = coeffList[i]
        
            newPm = applyPermutation(pm, perm, size)
            '''
            temp = (pm[0][0], pm[0][1], pm[1][0], pm[1][1], pm[2][0], pm[2][1])
            temp2 = []
            for number in temp:
                temp2.append(perm[number-1])


            permuted_pm = []
            if temp2[0] < temp2[1]:
                permuted_pm.append((temp2[0], temp2[1]))
            else:
                permuted_pm.append((temp2[1], temp2[0]))
            if temp2[2] < temp2[3]:
                permuted_pm.append((temp2[2], temp2[3]))
            else:
                permuted_pm.append((temp2[3], temp2[2]))
            if temp2[4] < temp2[5]:
                permuted_pm.append((temp2[4], temp2[5]))
            else:
                permuted_pm.append((temp2[5], temp2[4]))
            permuted_pm = sorted(permuted_pm)
            
            '''
            
            
            row_index = pmDict[pmToStr(newPm)]
            matrix[row_index][col_index] = coeff

    return matrix
            









# print matrix with leading term row by row

def printRowByRow(mat):
    strmatrix = []
    print('[')
    for i in range(len(mat)):
        strmatrix.append(' '.join(mat[i]).replace("'", ""))
        print(strmatrix[i])
    print(']')



# A.<b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15> = QQ[]
# print in forms of dependency polynomial
def generateDepEqnIdeal(leading_term, target_term):
    
    matrix = generateMat(leading_term,6)
    dependCoeff = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15']
    dependCoeff[target_term - 1] = '1'
    
    

    
    varStr = ''
    for i in range(target_term+1, 16):
        varStr += 'b'+str(i)+','
    for i in range(1, leading_term):
        varStr += 'a'+str(i)+','
    varStr = varStr[:-1]
    
    
    equationStr = ''
    
      
    for i in range(720):
        if (i == 0):
            equationStr += "A.<" + varStr + "> = GF(2)[]\nI1 = A.ideal("
        if (i == 255):
            equationStr += "I2 = A.ideal("
        if (i == 510):
            equationStr += "I3 = A.ideal("
        equationEmpty = 1
        for j in range(target_term - 1,15):
            
            if matrix[j][i] == '0':
                pass
            else:
                
                if matrix[j][i] == '1':
                    if (not equationEmpty):
                        equationStr += '+'
                    equationStr += dependCoeff[j]
                elif dependCoeff[j] == '1':
                    if (not equationEmpty):
                        equationStr += '+'
                    equationStr += matrix[j][i]
                else:
                    if (not equationEmpty):
                        equationStr += '+'
                    equationStr += dependCoeff[j] + '*' + matrix[j][i]
                    
                    
                equationEmpty = 0
        if (i == 254):
            equationStr += ")\n"
        elif (i == 509):
            equationStr += ")\n"
        elif (i == 719):
            equationStr += ")\n"
        else:
            if (not equationEmpty):
                equationStr += ',\n'
            
            
            
            
            
    equationStr += "I = I1+I2+I3\nprint '"+str(leading_term)+"_"+str(target_term)+"'\nprint I.groebner_basis()\n\n\n"
    with open(str(leading_term)+"-"+str(target_term)+"-Eqns.sage", "w") as text_file:
        text_file.write(equationStr)






#generateDepEqnIdeal(11,9)
#generateDepEqnIdeal(11,13)








# single permutation achievable graph

def directPermutable(matrix, leading_term, target_term, size):
    A = set()
    if (target_term <= leading_term) or (target_term > oddDoubleFactorial(size)):
        return False

    tempSet = set()
    passSet1 = {'1'}
    passSet2 = set()
    for m in range(leading_term-1):
        passSet2.add('a'+str(m+1))
    for j in range(factorial(size)):
    #if matrix[11][j] == '0' and matrix[14][j] == '1':
        #print(matrix[11][j], matrix[12][j], matrix[13][j], matrix[14][j])
    #if matrix[11][j] == '1' and matrix[14][j] == '0':
        #print(matrix[11][j], matrix[12][j], matrix[13][j], matrix[14][j])
    #if matrix[12][j] == '0' and matrix[14][j] == '1':
        #A.add((matrix[11][j], matrix[12][j], matrix[13][j], matrix[14][j]))
    #if matrix[12][j] == '1' and matrix[14][j] == '0':
        #A.add((matrix[11][j], matrix[12][j], matrix[13][j], matrix[14][j]))
        if matrix[target_term - 1][j] != '0':
            fail_flag = 0
            for k in range(target_term, oddDoubleFactorial(size)):
                if matrix[k][j] != '0':
                    fail_flag = 1
                    break
            if fail_flag == 0:
                #print(matrix[target_term - 1][j], 'target_term', target_term, j)
                tempSet.add(matrix[target_term - 1][j])
                #break
    if passSet1.issubset(tempSet) or passSet2.issubset(tempSet):
        return True
    else:
        return False

        


size = 8
temp = [1,2,3,6,9,13,15,17,18,23,24,25,26,30,31,32,33,34,41,45,51,59,60,68,69,73,76,79,82,83,85,86,89,91,93,103,105]
for i, leading_term in enumerate(temp):
    matrix = generateMat(leading_term, size)
    for target_term in temp[i+1:]:
        if directPermutable(matrix, leading_term, target_term,size):
            print(leading_term, target_term, 'pass')








# A5, A9, A10 subrepresentation for 6 point
'''
P1 = [[1,2,3], [1,2,4], [1,2,5], [1,2,6], [1,3,4], [1,3,5],
      [1,3,6], [1,4,5], [1,4,6], [1,5,6]]

matrix2 = []
for part1 in P1:
    row = [0] * 15
    P2 = list(itertools.permutations(list(set([1,2,3,4,5,6]) - set(part1))))
    for part2 in P2:
        fullPm = []
        for i in range(3):
            if part1[i] > part2[i]:
                fullPm.append((part2[i], part1[i]))
            else:
                fullPm.append((part1[i], part2[i]))
        fullPm = sorted(fullPm)
        sign = 0
        originalStr = ''.join(str(k) for k in P2[0])
        cycleStr = originalStr + originalStr
        permutedStr = ''.join(str(k) for k in part2)
        if permutedStr in cycleStr:
            sign = 1
        else:
            sign = -1
            
        row[index_dic[pmToStr(fullPm)]] = sign
    matrix2.append(row)
print(matrix2)
'''
'''

# A10



matrix2 = []
P1 = [[1,2],[1,3],[1,4],[1,5],[1,6],[2,3],[2,4],[2,5],
      [2,6],[3,4],[3,5],[3,6],[4,5],[4,6],[5,6]]
for part1 in P1:
    row = [0] * 15
    P2 = list(itertools.permutations(list(set([1,2,3,4,5,6]) - set(part1))))
    for part2 in P2:
        fullPm = [(part1[0], part1[1])]
        if part2[0] > part2[1]:
            continue
        if part2[2] > part2[3]:
            continue
        if part2[0] > part2[2]:
            continue
        fullPm.append((part2[0], part2[1]))
        fullPm.append((part2[2], part2[3]))
        fullPm = sorted(fullPm)
        row[index_dic[pmToStr(fullPm)]] = 1
    matrix2.append(row)
#print(matrix2)


# A9 require A10
matrix3 = []
for i in range(len(matrix2)):
    for j in range(i+1, len(matrix2), 1):
        row  = [0]*15
        for k in range(15):
            row[k] = matrix2[i][k] - matrix2[j][k]
        matrix3.append(row)
        
print("[")
for i in range(len(matrix3)):
    print(' '.join(str(k) for k in matrix3[i]))
print("]")

'''



# print possibility matrix
'''
subrepresentations = [
{15},
{9, 11, 12, 14, 15},
{9, 11, 12, 13, 14, 15},
{6, 7, 9, 10, 11, 12, 13, 14, 15},
{3, 6, 7, 9, 10, 11, 12, 13, 14, 15},
{2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15},
{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}]

# row index = first ptn, column index = second ptn
possibility = []
for i in range(15):
    row = [0]*15
    for j in range(i+1,15):
        for subrepSet in subrepresentations:
            if {i+1,j+1}.issubset(subrepSet):
                row[j] += 1
            elif {i+1}.issubset(subrepSet):
                row[j] = -1
                break
            elif {j+1}.issubset(subrepSet):
                row[j] = -1
                break
            else:
                row[j] += 0
            
    possibility.append(row)


print("[")
for i in range(len(possibility)):
    print(' '.join(str(k) for k in possibility[i]))
print("]")
'''