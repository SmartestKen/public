import numpy as np
import collections
import itertools



#Takes superpartition in lam a lam s form and returns a matrix with 1's as squares and -1's as circles.
def SuperPartition(La,Ls):
    ell = len(La)+len(Ls)
    if len(Ls) == 0:
        if len(La) == 0:
            L1 = 0
        else:
            L1 = La[0]+1
    else:
        if len(La) == 0:
            L1 = Ls[0]
        else:
            L1 = max(Ls[0],La[0]+1)
    Lstar = La + Ls
    Lstar.sort(reverse = True)
    Laplus1 = [p+1 for p in La]
    Lcircle = Laplus1 + Ls
    Lcircle.sort(reverse = True)
    T = np.zeros(shape =(ell+1,L1+1), dtype = np.int)
    for i in range(0,ell):
        for j in range(0,Lstar[i]):
            T[i,j] = 1
        if Lcircle[i] - Lstar[i] > 0:
            T[i,Lstar[i]] = -1
    return T

#Takes a superpartion in matrix format (see above) and returns
def dimensions(T):
    ell = len(T)-1
    L1 = len(T[0])-1
    return (ell,L1)

#Takes as input a list of superpartition in matrix format and an integer r and returns a list of all Vertical r-strips applied to
#all superpartitions in the list
#(this function may be obsolete)
def VerticalStrip(TL,r):
    if r == 0:
        return TL
    L = []
    for T in TL:
        ell,L1 = dimensions(T)
        j = 0
        SP = T.copy()
        while T[0,j] == 1:
            j = j + 1
        if SP[0,j] != 2:
            SP[0,j] = 2
            if SP[0,L1] != 0:
                    b = np.zeros((ell+1,L1+2), dtype = np.int)
                    b[:,:-1] = SP
                    SP = b
                    L.append(SP)
        for i in range(0,ell):
            SP = T.copy()
            j = 0
            while T[i,j] == 1:
                j = j+1
            if SP[i,j] != 2 and SP[i-1,j] != 0:
                SP[i,j] = 2
                L.append(SP)
        SP = T.copy()
        SP[ell,0] = 2
        zeros = [0 for i in range(0,L1+1)]
        SP = np.append(SP,[zeros],axis = 0)
        L.append(SP)
    return VerticalStrip(L,r-1)


#This draws a square centered at c with side length r
def DrawSquarePLT(r,c):
    return plt.Rectangle((c[0]-r/2,c[1]-r/2),r,r, fill = False)

#This draws a gray square centered at c with side length r (i think it actually colors it blue.)
def DrawGraySquarePLT(r,c):
    return plt.Rectangle((c[0]-r/2,c[1]-r/2),r,r)
#you get the idea
def DrawRedSquarePLT(r,c):
    return plt.Rectangle((c[0]-r/2,c[1]-r/2),r,r, color = 'red')
#draws a circle centered at c with diameter r
def DrawCirclePLT(r,c):
    return plt.Circle((c[0],c[1]),r/2, fill = False)
def DrawGrayCirclePLT(r,c):
    return plt.Circle((c[0],c[1]),r/2)


#This takes a list of superpartitions in the form [matrix,sign] and draws them all in a nXm array.
#if it is a negative sign then it draws a red square in the lower right corner.
#It gives you an error if nm < the number of superpartitions.
def drawTableauxPLT(TL,n,m):
    t = 1
    fig1 = plt.figure()
    for TP in TL:
        T = TP[0]
        sign = TP[1]
        ax = fig1.add_subplot(n,m,t)
        ax.axis('off')
        ell, L1 = dimensions(T)
        D = max(ell+1,L1+1)
        r = 1.0/D
        for i in range(0,ell):
            for j in range(0,L1):
                if T[i,j] > 0 and T[i,j] < 20:
                    S = DrawSquarePLT(r,(r*j+r,1-r*i-r))
                if T[i,j] < 0 and T[i,j] < 20:
                    S = DrawCirclePLT(r*0.8,(r*j+r,1-r*i-r))
                if T[i,j] == 20:
                    S = DrawGraySquarePLT(r*0.8,(r*j+r,1-r*i-r))
                if T[i,j] == -20:
                    S = DrawGrayCirclePLT(r*0.8,(r*j+r,1-r*i-r))
                ax.add_patch(S)
        if sign == -1:
             S = DrawRedSquarePLT(r,(r*(j+1)+r,1-r*(i+1)-r))
        ax.add_patch(S)
        t = t+1
    plt.show()




#This takes a list of superpartitions in the form [matrix,sign] and an integer r
#it returns the superpartitions in the expansion of S_L*e_r for all L in TL.
def sInfinityer(TL,r):
    if r == 0:
        return TL
    L = []
    for TP in TL:
        T = TP[0]
        sign = TP[1]
        ell, L1 = dimensions(T)
        h = ell
        while (20 not in T[h]) and h >= 0:
            h = h-1
        if h == -1:                 #this means there are no 20's yet
            j = 0
            SP = T.copy()
            while T[0,j] > 0:
                j = j + 1
            if SP[0,j] < 0:          #if there is a circle in the first row
                SP[0,j+1] = SP[0,j]  #move the circle over
            SP[0,j] = 20
            b = np.zeros((ell+1,L1+2), dtype = np.int)
            b[:,:-1] = SP
            SP = b
            L.append([SP,sign])
            h = h+1
        for i in range(h+1,ell):
            flag = 1   #this will change to 0 if there are two circles side by side
            SP = T.copy()
            j = 0
            while T[i,j] > 0:
                j = j + 1      #j is where the squares end
            if T[i,j-1] != 20 and SP[i-1,j] > 0:   # the square to the left must not be new and the cell above must be a square
                if T[i,j] < 0:                  #if the current entry is a circle then
                    SP[i,j+1] = SP[i,j]         #move it to the right one column
                    k = i-1                    #k will end up being the row that the circle "falls" into
                    while SP[k,j+1] == 0 and k >= 0:
                        SP[k,j+1] = SP[k+1,j+1]
                        SP[k+1,j+1] = 0
                        k = k-1
                    if SP[k,j+1] < 0:    #if we put a circle on top of another circle then
                        flag = 0
                    if SP[0,L1] != 0:
                        b = np.zeros((ell+1,L1+2), dtype = np.int)
                        b[:,:-1] = SP
                        SP = b
                SP[i,j] = 20
                if flag == 1:
                    L.append([SP,sign])
        if T[ell-1,0] > 0:              #if there is not a circle as the bottom most entry
            SP = T.copy()
            SP[ell,0] = 20
            zeros = [0 for i in range(0,L1+1)]
            SP = np.append(SP,[zeros],axis = 0)
            L.append([SP, sign])
    return sInfinityer(L,r-1)


    #This takes a list of superpartitions in the form [matrix,sign] and an integer r
#it returns the superpartitions in the expansion of S_L*(e_r)^~ for all L in TL.
def sInfinityerTwiddle(TL,r):
    SER = sInfinityer(TL,r)
    L = []
    for TP in SER:
        T = TP[0]
        sign = TP[1]
        ell,L1 = dimensions(T)
        if 20 not in T[0]:
            b = np.zeros((ell+1,L1+2), dtype = np.int)
            b[:,:-1] = T
            T = b
            j = 0
            while T[0,j] != 0:
                j = j + 1
            T[0,j] = -20
            if T[0,j-1] > 0:
                L.append([T,sign])
        else:
            flag = 1
            i = 0
            while 20 in T[i]:
                i = i + 1
            j = 0
            while T[i,j] != 0:
                j = j + 1
            if j == 0:
                T[i,j] = -20
            else:
                if T[i,j-1] < 0:
                    flag = 0
                else:
                    T[i,j] = -20
            for k in range(0,i):
                m = 0
                while T[k,m] != 0:
                    m = m+1
                if T[k,m-1] < 0:
                    sign = sign*(-1)
            if T[i-1,j] > 0:
                if T[ell,0] != 0:
                    zeros = [0 for i in range(0,L1+1)]
                    T = np.append(T,[zeros],axis = 0)
                if flag == 1:
                    L.append([T,sign])
    return L



#this takes in a sequence of integers for example [3,2,-3] and returns all the tableaux resulting from e3*e2*e3^~
#with the squares filled with 3 1's, 2 2's and 3 3's and one circle filled with 3.
def AllTableaux_e_Infinity(sequence_of_integers):
    SOI = sequence_of_integers
    Length = len(SOI)
    if SOI[0] > 0:
        SP = SuperPartition([],[1 for ii in range(0,SOI[0])])
    else:
        SP = SuperPartition([0],[1 for ii in range(0,-SOI[0])])
    L = [[SP,1]]
    for i in range(1,Length):
        if SOI[i] > 0:
            L = sInfinityer(L,SOI[i])
        if SOI[i] <= 0:
            L = sInfinityerTwiddle(L,-SOI[i])
        for TP in L:
            T = TP[0]
            ell, L1 = dimensions(T)
            for k in range(0,ell):
                for j in range(0,L1):
                    if T[k,j] == 20:
                          T[k,j] = i+1
                    if T[k,j] == -20:
                          T[k,j] = -(i+1)
    return L

'''
#takes a list of tableaux in matrix form with the matrices filled with the integers rather than just 0,1,-1.
#then it draws all of these in a nXm grid with fontsize = fs
def drawTableauxNumbersPLT(TL,n,m,fs):
    t = 1
    fig1 = plt.figure()
    for TP in TL:
        T = TP[0]
        sign = TP[1]
        ax = fig1.add_subplot(n,m,t)
        ax.axis('off')
        ell, L1 = dimensions(T)
        D = max(ell+1,L1+1)
        r = 1.0/D
        for i in range(0,ell):
            for j in range(0,L1):
                if T[i,j] > 0:
                    S = DrawSquarePLT(r,(r*j+r,1-r*i-r))
                if T[i,j] < 0:
                    S = DrawCirclePLT(r,(r*j+r,1-r*i-r))
                ax.add_patch(S)
                if T[i,j] != 0:
                    ax.text(r*j+r*0.8,1-r*i-r*1.2,T[i,j],fontsize = fs)
        if sign == -1:
             S = DrawRedSquarePLT(r,(r*(j+1)+r,1-r*(i+1)-r))
             ax.add_patch(S)
        t = t+1
    plt.show()
'''
#Basically the reverse of Superpartition, it takes a superpartition in matrix form and returns the lambda a, lambda s form.
def shape(T):
    ell, L1 = dimensions(T)
    La = []
    Ls = []
    for i in range(0,ell):
        j = 0
        while T[i,j] != 0:
            j = j + 1
        if T[i,j-1] < 0:
            La.append(j-1)
        else:
            Ls.append(j)
    return La,Ls

#I don't really remember what this does
def Type(T):
    F = T.flatten()
    CC = collections.Counter(F)
    print(CC)


#this does same as sInfinityer but with h's
def sInfinityhr(TL,r):
    if r == 0:
        return TL
    L = []
    for TP in TL:
        T = np.transpose(TP[0])
        sign = TP[1]
        ell, L1 = dimensions(T)
        h = ell
        while (20 not in T[h]) and h >= 0:
            h = h-1
        if h == -1:                 #this means there are no 20's yet
            j = 0
            SP = T.copy()
            while T[0,j] > 0:
                j = j + 1
            if SP[0,j] < 0:          #if there is a circle in the first row
                SP[1,j] = SP[0,j]  #move the circle down
                SP[0,j] = 20
                k = j-1
                while SP[1,k] == 0 and k >= 0:
                    SP[1,k] = SP[1,k+1]
                    SP[1,k+1] = 0
                    k = k-1
                if SP[1,k] >= 0:
                    if SP[ell,0] != 0:
                        zeros = [0 for i in range(0,L1+1)]
                        SP = np.append(SP,[zeros],axis = 0)
                    L.append([np.transpose(SP),sign])
            else:
                SP[0,j] = 20
                b = np.zeros((ell+1,L1+2), dtype = np.int)
                b[:,:-1] = SP
                SP = b
                L.append([np.transpose(SP),sign])
            h = h+1
        for i in range(h+1,ell):
            flag = 1   #this will change to 0 if there are two circles side by side
            SP = T.copy()
            j = 0
            while T[i,j] > 0:
                j = j + 1      #j is where the squares end
            if T[i,j-1] != 20 and SP[i-1,j] > 0:   # the square to the left must not be new and the cell above must be a square
                if T[i,j] < 0:                  #if the current entry is a circle then
                    SP[i+1,j] = SP[i,j]         #move it down one row
                    k = j-1                    #k will end up being the column that the circle "falls" into
                    while SP[i+1,k] == 0 and k >= 0:
                        SP[i+1,k] = SP[i+1,k+1]
                        SP[i+1,k+1] = 0
                        k = k-1
                    if SP[i+1,k] < 0:    #if we put a circle on top of another circle then
                        flag = 0
                    if SP[0,L1] != 0:
                        b = np.zeros((ell+1,L1+2), dtype = np.int)
                        b[:,:-1] = SP
                        SP = b
                SP[i,j] = 20
                if SP[ell,0] != 0:
                    zeros = [0 for i in range(0,L1+1)]
                    SP = np.append(SP,[zeros],axis = 0)
                if flag == 1:
                    L.append([np.transpose(SP),sign])
        if T[ell-1,0] > 0:              #if there is not a circle as the bottom most entry
            SP = T.copy()
            SP[ell,0] = 20
            zeros = [0 for i in range(0,L1+1)]
            SP = np.append(SP,[zeros],axis = 0)
            L.append([np.transpose(SP), sign])
    return sInfinityhr(L,r-1)


#this does the same as sInfinityer but with s^0
def sZeroer(TL,r):
    if r == 0:
        return TL
    L = []
    for TP in TL:
        T = TP[0]
        sign = TP[1]
        ell, L1 = dimensions(T)
        h = ell
        while (20 not in T[h]) and h >= 0:
            h = h-1
        if h == -1:                 #this means there are no 20's yet
            j = 0
            SP = T.copy()
            while T[0,j] != 0:       #j will be set to the first column without a square or a circle
                j = j + 1
            if SP[0,j-1] < 0:          #if there is a circle in the first row
                SP[0,j] = SP[0,j-1]  #move the circle over
                SP[0,j-1] = 20
            else:
                SP[0,j] = 20
            b = np.zeros((ell+1,L1+2), dtype = np.int)
            b[:,:-1] = SP
            SP = b
            L.append([SP,sign])
            h = h+1
        for i in range(h+1,ell):
            flag = 1   #this will change to 0 if there are two circles side by side
            SP = T.copy()
            j = 0
            while T[i,j] != 0:
                j = j + 1      #j is set to the first column without a square or a circle
            if T[i,j-1] != 20 and SP[i-1,j] != 0:   # the square to the left must not be new and the cell above must not be empty
                if T[i,j-1] < 0:                  #if cell to the left is a circle then...
                    SP[i,j] = SP[i,j-1]         #move it to the right one column
                    SP[i,j-1] = 20
                    if SP[i-1,j] < 0:    #if we put a circle on top of another circle then
                        flag = 0
                    if SP[0,L1] != 0:
                        b = np.zeros((ell+1,L1+2), dtype = np.int)
                        b[:,:-1] = SP
                        SP = b
                if T[i-1,j] < 0:                 #if the cell above is a circle, then.......
                    SP[i,j] = SP[i-1,j]          #move it down
                    SP[i-1,j] = 20
                if T[i-1,j] > 0 and T[i,j-1] > 0:    #if there are no circles touching the new square then don't move anything
                    SP[i,j] = 20
                if flag == 1:
                    L.append([SP,sign])
        SP = T.copy()
        if SP[ell-1,0] < 0:             #if there is a circle as the bottom cell
            SP[ell,0] = SP[ell-1,0]
            SP[ell-1,0] = 20
        if T[ell-1,0] > 0:              #if there is not a circle as the bottom most entry
            SP[ell,0] = 20
        zeros = [0 for i in range(0,L1+1)]
        SP = np.append(SP,[zeros],axis = 0)
        L.append([SP, sign])
    return sZeroer(L,r-1)

#same as above but with e^~
def sZeroerTwiddle(TL,r):
    SER = sZeroer(TL,r)
    L = []
    for TP in SER:
        T = TP[0]
        sign = TP[1]
        ell,L1 = dimensions(T)
        h = ell
        if 20 not in T:
            SP = T.copy()
            b = np.zeros((ell+1,L1+2), dtype = np.int)
            b[:,:-1] = SP
            SP = b
            j = 0
            while SP[0,j] != 0:
                j = j + 1
            SP[0,j] = -20
            if SP[0,j-1] > 0:
                L.append([SP,sign])
        while (20 not in T[h]) and h >= 0:
            h = h-1
        h = h+1
        for i in range(h,ell-1):
            SP = T.copy()
            sign = TP[1]
            flag = 1
            j = 0
            while T[i,j] > 0:
                j = j + 1
            if T[i,j] == 0 and T[i-1,j] > 0:
                SP[i,j] = -20
                for k in range(0,i):
                    m = 0
                    while T[k,m] != 0:
                        m = m+1
                        if T[k,m-1] < 0:
                            sign = sign*(-1)
                L.append([SP,sign])
        if T[ell-1,0] > 0:
            SP = T.copy()
            sign = TP[1]
            for k in range(0,ell):
                m = 0
                while T[k,m] != 0:
                    m = m+1
                    if T[k,m-1] < 0:
                        sign = sign*(-1)
            SP[ell,0] = -20
            zeros = [0 for i in range(0,L1+1)]
            SP = np.append(SP,[zeros],axis = 0)
            L.append([SP,sign])
    return L


#Same as alltableaux e infinity but with s^0
def AllTableaux_e_Zero(sequence_of_integers):
    SOI = sequence_of_integers
    Length = len(SOI)
    if SOI[0] > 0:
        SP = SuperPartition([],[1 for ii in range(0,SOI[0])])
    else:
        SP = SuperPartition([0],[1 for ii in range(0,-SOI[0])])
    L = [[SP,1]]
    for i in range(1,Length):
        if SOI[i] > 0:
            L = sZeroer(L,SOI[i])
        if SOI[i] <= 0:
            L = sZeroerTwiddle(L,-SOI[i])
        for TP in L:
            T = TP[0]
            ell, L1 = dimensions(T)
            for k in range(0,ell):
                for j in range(0,L1):
                    if T[k,j] == 20:
                          T[k,j] = i+1
                    if T[k,j] == -20:
                          T[k,j] = -(i+1)
    return L


#Same as szeroer but with h's
def sZerohr(TL,r):
    T = sZeroer(TL,r)
    L = []
    for t in T:
        SP = np.transpose(t[0])
        L.append([SP,t[1]])
    return L

#Same as szeroer^~ but with h's
def sZerohrTwiddle(TL,r):
    T = sZeroerTwiddle(TL,r)
    L = []
    for t in T:
        SP = np.transpose(t[0])
        L.append([SP,t[1]])
    return L

#same as alltableaux e zero but with h's
def AllTableaux_h_Zero(sequence_of_integers):
    T = AllTableaux_e_Zero(sequence_of_integers)
    L = []
    for t in T:
        SP = np.transpose(t[0])
        L.append([SP,t[1]])
    return L

#All partitions of n into up to m parts
def Parts(n,m):
    if n == m:
        return [[n]] + Parts(n,m-1)
    if m == 0 or n < 0:
        return []
    if n == 0 or m == 1:
        return [[1 for i in range(0,n)]]
    return list(map(lambda x: [m] + x, Parts(n-m,m))) + Parts(n,m-1)


#All partitions of n
def AllPartitions(n):
    return Parts(n,n)


#I think this gives all possible ways to fill the superpartition La,Ls?
def AllSuperFillings(La,Ls):
    m = len(La)
    N = sum(La)+sum(Ls)
    AP = list(map(lambda x: x+[0],AllPartitions(N)))
    L = []
    for ap in AP:
        s = set(ap)
        if len(s) >= m:
            for ss in list(itertools.combinations(list(s),m)):
                p = list(ap)
                for i in ss:
                    p[p.index(i)] = -p[p.index(i)]
                p.sort()
                p = p[0:m]+list(reversed(p[m:len(p)]))
                if len(p) > m and p[-1] == 0:
                    L.append(p[:-1])
                else:
                    L.append(p)
    return L

#this gives all SYT of the superpartition La,Ls in relation to s^0
def AllFillingsZero(La,Ls):
    ASF = AllSuperFillings(La,Ls)
    L = []
    for sp in ASF:
        AThZ = AllTableaux_h_Zero(sp)
        for T in AThZ:
            if shape(T[0]) == (La,Ls):
                L.append(T)
    return L


#This is basically just the transposes of all of the results from sInfinityer
def sInfStarhr(TL,r):
    T = sInfinityer(TL,r)
    L = []
    for t in T:
        SP = np.transpose(t[0])
        L.append([SP,t[1]])
    return L

#This is basically just the transposes of all of the results from sInfinityerTwiddle
def sInfStarhrTwiddle(TL,r):
    T = sInfinityerTwiddle(TL,r)
    L = []
    for t in T:
        SP = np.transpose(t[0])
        L.append([SP,t[1]])
    return L

#Basically all the transposes of AllTableaux e Infinity.
#(note on this is that it considers the SYT to be weakly increasing in rows and strictly in columns)
def AllTableaux_h_InfinityStar(sequence_of_integers):
    T = AllTableaux_e_Infinity(sequence_of_integers)
    L = []
    for t in T:
        SP = np.transpose(t[0])
        L.append([SP,t[1]])
    return L

#All transposes of s^inf but weakly increasing in rows and strictly in colunms
def AllFillingsInfinityStar(La,Ls):
    ASF = AllSuperFillings(La,Ls)
    L = []
    for sp in ASF:
        AThIS = AllTableaux_h_InfinityStar(sp)
        for T in AThIS:
            if shape(T[0]) == (La,Ls):
                L.append(T)
    return L

#this takes in the content of the two-row notation and produces all possible pairs (P,Q) of syt that could correspond to it.
def RSK_possibilities(Q_row,P_row):
    possible_Q = AllTableaux_h_Zero(Q_row)
    possible_P = AllTableaux_e_Infinity(P_row)
    output = []
    for i in possible_Q:
        for j in possible_P:
            if shape(i[0]) == shape(j[0]):
                output = output + [[i,j]]

    for p in output:
        print(p[0][0])
        print(p[1][0])
        if p is not output[-1]:
            print("----------------")






# size = side length
def matToArray(mat, size):
    P = []
    Q = []

    for idx, element in enumerate(A):
            if element > 0:
                Q.append(idx//size+1)
                P.append(idx%size+1)
            elif element < 0:
                Q.append(-(idx//size+1))
                P.append(-(idx%size+1))
    return [Q,P]

# input, two row array (first Q, then P)
def arrayTohseq(trarray, size):
    collector_Q = [0]*size
    sgn_Q = [1]*size
    collector_P = [0]*size
    sgn_P = [1]*size

    for i in range(len(trarray[0])):

        # ask miles, we may want to include circle as a square*-1 since there may be multiple circles
        if trarray[0][i] < 0:
            sgn_Q[abs(trarray[0][i])-1] = -1
            sgn_P[abs(trarray[1][i])-1] = -1

        collector_Q[abs(trarray[0][i])-1] += 1
        collector_P[abs(trarray[1][i])-1] += 1


    hseq_Q = list(filter(lambda a: a != 0, [i*j for i,j in zip(collector_Q, sgn_Q)]))
    hseq_P = list(filter(lambda a: a != 0, [i*j for i,j in zip(collector_P, sgn_P)]))

    hseq_Q = [i+1 if i<0 else i for i in hseq_Q]
    hseq_P = [i+1 if i<0 else i for i in hseq_P]
    #print(hseq_Q, hseq_P)
    return [hseq_Q, hseq_P]

def RSK_path(trarrays, size):
    # trarrays = matToArray(mat,size)
    for i in range(len(trarrays[0])):
        trarrays_temp = [trarrays[0][:(i+1)], trarrays[1][:(i+1)]]
        hseqs_temp = arrayTohseq(trarrays_temp, size)
        print("--hseq:", hseqs_temp, "correspond to", trarrays_temp)


        RSK_possibilities(hseqs_temp[0], hseqs_temp[1])
        print("---------end of hseq------------")


# both input are array, return true if a is a subshape of b
# assuming all zero at the end
def isSubShape(a, b):

    try:
        for i in range(len(a)):
            nonzero_ai = [x for x in a[i] if x != 0]
            nonzero_bi = [x for x in b[i] if x != 0]
            if len(nonzero_ai) > len(nonzero_bi):
                return False
        return True

    except:
        # at here, it means exceed b's range
        return False





# both input are array, return true if a is a subtableau of b
def isSubTableau(a, b):
    try:
        for i in range(len(a)):
            for j in range(len(a[i])):
                if a[i][j] == 0:
                    break
                if a[i][j] != b[i][j]:
                    return False
        return True

    except:
        # at here, it means b exceed the range
        return False





# idx//len+1 idx %len+
A = [1, 0, 0, -1, 1, 1, 1, -1, 0]
arrays = matToArray(A,3)

# print(arrays[0], arrays[1])
# RSK_path(arrays,3)
RSK_path([[1, 1, -2, 3, 3], [1, 3, -1, 2, 3]],3)
# [2,0,2],[-1,1,2],


print(isSubShape([[1,3,-1,0],[2,0,0,0],[0,0,0,0]], [[1,2,-1,0],[2,3,0,0],[0,0,0,0]]))
print(isSubTableau([[1,3,-1,0],[2,0,0,0],[1,0,0,0]], [[1,3,-1,0],[2,3,0,0],[1,1,2,0]]))



