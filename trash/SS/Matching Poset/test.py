# start by calling subPartition(lda, 0)
def subPartition(shape, curRow):

    # base case, last row -> select or not select
    if curRow == len(shape)-1:
        mu1 = list(shape)
        mu2 = list(shape)
        mu2[-1] -= 1
        if mu2[-1] == 0:
            del mu2[-1]
            return [mu1, mu2]
        else:
            return [mu1] + subPartition(mu2, curRow)

    # not last row, if curRow not selectable
    if shape[curRow] == shape[curRow+1]:
        return subPartition(shape, curRow+1)
    # else, can choose to
    # not select and jump to next line, or select and stay at current line
    else:
        mu2 = list(shape)
        mu2[curRow] -= 1
        # [mu1] +
        return subPartition(shape, curRow+1) + subPartition(mu2, curRow)



print(subPartition([4,3,1],0))