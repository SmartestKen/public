from sage.all import *



# lda for standard tableau
# return: first index -> descent_size
# second index -> given each descent_size, the q polynomial
def majorIndex(lda):

    total = sum(lda)
    # d_size from [0, n]
    majList = [[0 for x in range(total*(total+1)//2)] for y in range(total+1)]
    ST_list = StandardTableaux(lda).list();
    for ST in ST_list:
        descent = getDescent(ST, lda)
        majList[len(descent)][sum(descent)] += 1


    for d_size in range(len(majList)):
        while len(majList[d_size]) > 0 and not majList[d_size][-1]:
            majList[d_size].pop()

    # symmetric so no need to reverse
    return majList


def getDescent(ST):
    lda = []
    for i in range(len(ST)):
        lda.append(len(ST[i]))
    descent = set()
    currRow = len(lda)-1
    currCol = lda[currRow]-1
    # roster -> something below
    # temp_roster _> something in the same row
    # but current row scanning not finished yet
    roster = set()
    temp_roster = set()
    while True:
        if currCol == -1:
            currRow -= 1
            roster = roster.union(temp_roster)
            temp_roster = set()
            if currRow == -1:
                break
            currCol = lda[currRow]-1


        num = ST[currRow][currCol]
        if num+1 in roster:
            descent.add(num)
        temp_roster.add(num)
        currCol -= 1
    return descent


# print(getDescent([[1,3],[2]],[2,1]))
# print(getDescent([[1,2],[3]],[2,1]))


def list_f(n, k):

    result = majorIndex([n,k])
    for i in range(n+1):
        q = polygen(ZZ, name='q')
        if result[i] == (q**(i**2)*(gaussian_binomial(n,i)*gaussian_binomial(k,i)-
        gaussian_binomial(n+1,i)*gaussian_binomial(k-1,i))).list():
            pass


# start by calling subPartition(lda, 0)
def subPartition(lda, curRow):

    # base case, last row -> select or not select
    if curRow == len(lda)-1:
        mu1 = list(lda)
        mu2 = list(lda)
        mu2[-1] -= 1
        if mu2[-1] == 0:
            del mu2[-1]
            return [mu1, mu2]
        else:
            return [mu1] + subPartition(mu2, curRow)

    # not last row, if curRow not selectable
    if lda[curRow] == lda[curRow+1]:
        return subPartition(lda, curRow+1)
    # else, can choose to
    # not select and jump to next line, or select and stay at current line
    else:
        mu2 = list(lda)
        mu2[curRow] -= 1
        # [mu1] +
        return subPartition(lda, curRow+1) + subPartition(mu2, curRow)














# R.<q,t> = PolynomialRing(ZZ)
# q = polygen(ZZ, name='q')
# t = polygen(QQ, name='t')
# R = PolynomialRing(ZZ,2,"qt")

# toggle 0-> remove 1, 1->remove q
def schur_exp(lda, toggle):
    q = var('q')
    t = var('t')
    LHS = 0
    RHS = 0
    muList = subPartition(lda, 0)
    for mu in muList:
        # dmList -> descent-major list
        dmList = majorIndex(mu)
        if mu == lda:
            for i in range(len(dmList)):
                for j in range(len(dmList[i])):
                    LHS += dmList[i][j]*(q**j)*(t**i)
        elif toggle == 1:
            temp = 1
            abslda = sum(lda)
            absmu = sum(mu)
            skew = abslda-absmu
            for i in range(len(dmList)):
                for j in range(len(dmList[i])):
                    temp += dmList[i][j]*(q**j)*((q**skew*t)**i)

            for i in range(1, skew):
                temp *= (1-(q**i)*t)
            temp *= t
            # print(temp)
            RHS += temp

        else:
            temp = 1
            for i in range(len(dmList)):
                for j in range(len(dmList[i])):
                    temp += dmList[i][j]*(q**j)*(t**i)
            abslda = sum(lda)
            absmu = sum(mu)
            for i in range(absmu+1, abslda):
                temp *= (1-(q**i)*t)
            temp *= (q**absmu)*t
            # print(temp)
            RHS += temp

    print(LHS.simplify_rational())
    print(RHS.simplify_rational())

schur_exp([4,3,1],1)
'''



n = 4
k = 3
m = 3
i = 3
q = polygen(ZZ, name='q')
print(majorIndex([n,k,m]))






product  = q**(k+i**2-(m+1)*(i-m))*(1-q**(n-k+1))*gaussian_binomial(k, i-m)*gaussian_binomial(n+1,i-m)
print(product)
print(R(majorIndex([n,k,m])[i])/product)
Waha = (R(majorIndex([n,k,m])[i])*(-q**3 + q))/product
print("---------------")
print(product.factor())
print(Waha/(1-q))
print(factor(Waha))
'''


