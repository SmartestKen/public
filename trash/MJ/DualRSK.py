# R1, row1, R2, row2, produce
# R1 sorted
# P isnertion, Q recording, initial call [] []
def DualRSK(R1,R2,P,Q):
    if len(R1) != len(R2):
        return "not valid"
    if len(R1) == 0:
        return [P,Q]
    else:
        DRSKinsert(R2[0], R1[0], P, Q)
        return DualRSK(R1[1:], R2[1:], P, Q)



def DRSKinsert(bump,stick,P,Q):
    print("before ", P,Q, "bump ", bump)
    currRow = 0
    while True:
        # edge case (out of bound)
        if currRow > len(P)-1:
            P.append([bump])
            Q.append([stick])
            break

        # not out of bound
        isBumped = False
        for idx, num in enumerate(P[currRow]):
            if num >= bump:
                print(bump, " bumps ", num, " at ", currRow, idx)
                bump_temp = num
                P[currRow][idx] = bump
                bump = bump_temp
                isBumped = True
                break
        # append at the end and stop
        if not isBumped:
            P[currRow].append(bump)
            Q[currRow].append(stick)
            break

        currRow += 1
    print("after ",P,Q)


# going back
def DualRSKReverse(P, Q, R1, R2):

    while len(P) != 0:

        # get the rightmost entry of max value in Q
        max = 0
        maxRow = -1
        for i in range(len(Q)):
            if Q[i][-1] > max:
                max = Q[i][-1]
                maxRow = i


        print(P[maxRow][-1], Q[maxRow][-1])
        R1.insert(0, Q[maxRow].pop())

        bump = P[maxRow].pop()
        if len(Q[maxRow]) == 0:
            del Q[maxRow]
            del P[maxRow]



        # bump it back
        currRow = maxRow-1
        while currRow >= 0:
            isBumped = False
            # bump the rightmost small or equal to num
            for idx, num in enumerate(P[currRow]):
                # there is at least one number in the row above that
                # is smaller or equal to bump (property of SSYT)
                if num > bump:
                    bump_temp = P[currRow][idx-1]
                    P[currRow][idx-1] = bump
                    bump = bump_temp
                    isBumped = True
                    break

            # everything smaller or equal to bump
            if not isBumped:
                bump_temp = P[currRow][-1]
                P[currRow][-1] = bump
                bump = bump_temp

            currRow -= 1
        R2.insert(0, bump)
        print(P,Q)


    return [R1,R2]


tableauList = DualRSK([-1,1,1,2,2,3,3,4,4],[-1,1,2,1,3,2,3,1,4], [], [])
DualRSKReverse(tableauList[0], tableauList[1], [], [])
