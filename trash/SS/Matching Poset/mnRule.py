'''
all input are assumed to be list of integers
pass [] to mu if not applicable
- perform init check
- return getPsi with empty refDict
'''
'''
do not use "sum" as a variable in any of your script,
otherwise the following error will occur
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: 'int' object is not callable
'''
debugToggle = False

def initGetPsi(lda, mu, alpha):
    global debugToggle

    if len(lda) >= len(mu):
        # padding mu with zero (same length with lda)
        mu += [0]*(len(lda)-len(mu))
    else:
        return None


    # ensure lda and mu are integer partition
    for i in range(1, len(lda)):
        if lda[i] > lda[i-1] or mu[i] > mu[i-1] or \
            lda[i] < 0 or mu[i] < 0:
            return None

    # ensure alpha is a weak composition
    for i in range(1, len(alpha)):
        if alpha[i] < 0:
            return None



    expectedBlocks = sum(alpha)

    # ensure each row interval exists
    for i in range(len(lda)):
        if mu[i] > lda[i]:
            return None
        else:
            expectedBlocks -= lda[i]-mu[i]

    # ensure sum(lda)-sum(mu)=sum(alpha)
    if expectedBlocks != 0:
        return None

    if debugToggle:
        print("pass all check")
    return getPsi(lda, mu, alpha, {"[][][]": 1})





'''

if exist in refDict, just return that psi
else (inherently dfs)
    get each possibility (remain + strip), call
    getPsi(remain) * (-1)^strip_height and sum
    all these possibility up
    store and return the new Psi
'''

# at this point, assume mu[i] <= lda[i]
def getPsi(lda, mu, alpha, refDict):

    global debugToggle
    # return None if not connected
    # if diminish case occur (normal check useless) and all later rows also
    # diminish, then good
    # if diminish case occur (normal check useless) and some later rows do
    # not diminish, then bad
    # if diminish case do not occur, then good/bad depends on normal check
    if debugToggle:
        print("start ", lda, mu, alpha)
    diminishFlag = False
    magnitude = []
    connection = []


    i = 0
    while i < len(lda):
    # diminish occur
        if lda[i] == mu[i]:
            diminishFlag = True
            del lda[i]
            del mu[i]

        # diminish do not occur, normal check
        # (whether last interval overlaps with current interval)
        # and append to shape arrays (magnitude/connection)

        else:
            magnitude.append(lda[i] - mu[i])
            if i > 0:
                if diminishFlag:
                    connection.append(0)
                    diminishFlag = False
                else:
                    connection.append(lda[i] - mu[i-1])
            i += 1






    # at this point, assume lda/mu valid and all
    # magnitude is non-zero
    if debugToggle:
        print("afterTrim ", lda, mu, alpha)
    refPsi = refDict.get(str(magnitude)+str(connection)+str(alpha), None)
    if refPsi is not None:
        if debugToggle:
            print("refDict am used")
        return refPsi


    # at this point nothing is found in refPsi, which
    # also ensures non empty magnitude
    max_width_index = lda[0]-1
    max_height_index = len(lda)-1

    # start finding border (row, col) (index 0 based)
    border = []
    numBlocks = []

    currentPt = (0, max_width_index)
    # borderEnd = (max_height_index, mu[max_height_index])
    # extra pt at the end of border
    extraPt = (max_height_index, mu[max_height_index]-1)

    while currentPt != extraPt:
        # good pt
        if currentPt[1] >= mu[currentPt[0]]:
            border.append(currentPt)
        # bad pt (in mu)
        else:
            border.append(currentPt)
            numBlocks += list(range(len(border)-len(numBlocks)-1, -1, -1))

        # if can go down
        if currentPt[0] < max_height_index and currentPt[1] == lda[currentPt[0]+1]-1:
            currentPt = (currentPt[0]+1, currentPt[1])
        # cannot go down, then go left
        else:
            currentPt = (currentPt[0], currentPt[1]-1)

    # append the extra bad block
    border.append(extraPt)
    numBlocks += list(range(len(border)-len(numBlocks)-1, -1, -1))




    # possible start point's index in border list
    # nothing to the right and is a good pt
    start = [0]
    for i in range(1, len(border)):
        if border[i][1]+1 == lda[border[i][0]] and numBlocks[i] > 0:
            start.append(i)



    # use those points to derive possible subTableaux
    # notice that the extra point ensures that ptIndex + numBlocks[ptIndex]
    # at any start pt always stays in border
    length = alpha[0]
    psi = 0
    for ptIndex in start:
        if length <= numBlocks[ptIndex]:
            if border[ptIndex+length][1] < border[ptIndex+length-1][1]:
                subLda = list(lda)
                subMu = list(mu)
                for i in range(ptIndex, ptIndex+length):
                    subLda[border[i][0]]-=1


                # no need to check length of alpha, [1:] won't throw an error

                subPsi = getPsi(subLda, subMu, alpha[1:], refDict)
                stripHeight = border[ptIndex+length-1][0]-border[ptIndex][0]
                psi += subPsi*(-1)**stripHeight



    refDict[str(magnitude)+str(connection)+str(alpha)] = psi
    return psi


