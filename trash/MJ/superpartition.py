import numpy as np
import matplotlib.pyplot as plt

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

def dimensions(T):
    ell = len(T)-1
    L1 = len(T[0])-1
    return (ell,L1)

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


def DrawSquarePLT(r,c):
    return plt.Rectangle((c[0]-r/2,c[1]-r/2),r,r, fill = False)

def DrawGraySquarePLT(r,c):
    return plt.Rectangle((c[0]-r/2,c[1]-r/2),r,r)
def DrawRedSquarePLT(r,c):
    return plt.Rectangle((c[0]-r/2,c[1]-r/2),r,r, color = 'red')

def DrawCirclePLT(r,c):
    return plt.Circle((c[0],c[1]),r/2, fill = False)
def DrawGrayCirclePLT(r,c):
    return plt.Circle((c[0],c[1]),r/2)


def drawTableauxPLT(TL):
    t = 1
    fig1 = plt.figure()
    for TP in TL:
        T = TP[0]
        sign = TP[1]
        ax = fig1.add_subplot(5,5,t)
        ax.axis('off')
        ell, L1 = dimensions(T)
        D = max(ell+1,L1+1)
        r = 1.0/D
        for i in range(0,ell):
            for j in range(0,L1):
                if T[i,j] == 1:
                    S = DrawSquarePLT(r,(r*j+r,1-r*i-r))
                if T[i,j] == -1:
                    S = DrawCirclePLT(r,(r*j+r,1-r*i-r))
                if T[i,j] == 20:
                    S = DrawGraySquarePLT(r,(r*j+r,1-r*i-r))
                if T[i,j] == -20:
                    S = DrawGrayCirclePLT(r,(r*j+r,1-r*i-r))
                ax.add_patch(S)
        if sign == -1:
             S = DrawRedSquarePLT(r,(r*(j+1)+r,1-r*(i+1)-r))
        ax.add_patch(S)
        t = t+1        
    plt.show()
    

def sInfinityer(TL,r):
    if r == 0:
        return TL
    L = []
    for TP in TL:
        T = TP[0]
        sign = TP[1]
        ell,L1 = dimensions(T)
        h = ell+1                           #h is set to the highest row with a 20
        while (20 not in T[h]) and h >= 0:
            h = h-1
        if h == -1:
            j = 0
            SP = T.copy()
            while T[0,j] == 1:
                j = j + 1
            if SP[0,j] != 20:
                if SP[0,j] < 0:
                    SP[0,j+1] = SP[0,j]
                SP[0,j] = 20
                if SP[0,L1] != 0:
                        b = np.zeros((ell+1,L1+2), dtype = np.int)
                        b[:,:-1] = SP
                        SP = b
                        L.append([SP,sign])
        for i in range(h,ell+1):
            flag = 1
            SP = T.copy()
            j = 0                    #find out where the squares stop
            while T[i,j] > 0:
                j = j+1
            if SP[i,j] != 20 and SP[i-1,j] > 0:
                if SP[i,j] < 0:
                    SP[i,j+1] = SP[i,j]
                    k = i-1
                    while SP[k,j+1] == 0 and k >= 0:
                        SP[k,j+1] = SP[k+1,j+1]
                        SP[k+1,j+1] = 0
                        k = k-1
                    if SP[k,j+1]<0:
                        flag = 0
                    if SP[0,L1] != 0:
                        b = np.zeros((ell+1,L1+2), dtype = np.int)
                        b[:,:-1] = SP
                        SP = b
                SP[i,j] = 20
                if flag == 1:
                    if SP[ell,0] != 0:
                        zeros = [0 for i in range(0,L1+1)]
                        SP = np.append(SP,[zeros],axis = 0)
                    L.append([SP, sign])
    return sInfinityer(L,r-1)


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
        i = 0
        while 20 in T[i]:
            i = i + 1
        j = 0
        while T[i,j] != 0:
            j = j + 1
        T[i,j] = -20
        for k in range(0,i):
            m = 0
            while T[k,m] != 0:
                m = m+1
            if T[k,m-1] < 0:
                sign = sign*(-1)
        if T[i,j-1] > 0:
            L.append([T,sign])
    return L


def AllTableaux_e_Infinity(sequence_of_integers):
    SOI = sequence_of_integers
    Length = len(SOI)
    if SOI[0] > 0:
        SP = SuperPartition([],[SOI[0]])
    else:
        SP = SuperPartition([SOI[0]],[])
    L = [[SP,1]]
    for i in range(1,Length):
        if SOI[i] > 0:
            L = sInfinityer(L,SOI[i])
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
            


def drawTableauxNumbersPLT(TL):
    t = 1
    fig1 = plt.figure()
    for TP in TL:
        T = TP[0]
        sign = TP[1]
        ax = fig1.add_subplot(5,5,t)
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
                    ax.text(r*j+r*0.8,1-r*i-r*1.2,T[i,j],fontsize = r*50)
        if sign == -1:
             S = DrawRedSquarePLT(r,(r*(j+1)+r,1-r*(i+1)-r))
             ax.add_patch(S)
        t = t+1        
    plt.show()
