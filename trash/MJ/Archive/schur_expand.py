import copy

# lda used for tableaux, numVar is the number of variables
def schur_expand(lda_temp, numVar_temp):

    global lda
    global numVar
    lda = lda_temp
    numVar = numVar_temp
    # init then each expand to the entire tableaux using recursive algo

    tableau = []
    # initialize a tableau
    for i in range(len(lda)):
        tableau.append([-1]*lda[i])

    return fill(tableau, len(lda)-1, lda[-1]-1)









def fill(tableau, currRow, currCol):

    global lda
    global numVar

    # print(currRow, currCol, tableau)

    result = set()

    if currRow != 0 or currCol != -1:



        if currCol == -1:
            currRow -= 1
            currCol = lda[currRow]-1

        maxNum = numVar-1

        # if not the last row and has something below
        if len(lda) > currRow+1 and lda[currRow+1] > currCol:
            maxNum = tableau[currRow+1][currCol]-1
        # if not the last column
        if lda[currRow] > currCol+1:
            maxNum = min(maxNum, tableau[currRow][currCol+1])

        # print(maxNum)
        for choice in range(maxNum+1):
            tableau[currRow][currCol] = choice
            result = result.union(fill(copy.deepcopy(tableau), currRow, currCol-1))


    else:

        monomial = [0]*numVar
        for i in range(len(tableau)):
            for j in range(len(tableau[i])):
                monomial[tableau[i][j]] += 1

        result.add(tuple(monomial))
        print("I return", list(result), tableau)


    return result



# schur_expand([2,1],3)
schur_expand([3,2],3)