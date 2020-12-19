# lda superpartition from s0 (format is (box_circle, box only)), num from e
def sinf_multiply_e(lda, num):

    box_circle = lda[0]
    box_only = lda[1]


    # check if box_circle part equal/longer than box_only
    length_diff = len(box_circle)-len(box_only)
    if length_diff != 0 and length_diff != 1:
        return None

    # pad box only part with 0 so that length is consistent
    box_only += [0]*(length_diff)

    # check 1. within each part the length is non-increasing each row
    # 2. each row (box_circle - box_only) = 0 or 1 (box_only
    # contained in box_circle)
    if (box_circle[0]-box_only[0]) != 0 and (box_circle[0]-box_only[0]) != 1:
        return None

    for i in range(1, len(box_circle)):
        if box_circle[i] > box_circle[i-1]:
            return None
        if box_only[i] > box_only[i-1]:
            return None
        if (box_circle[i]-box_only[i]) != 0 and (box_circle[i]-box_only[i]) != 1:
            return None


    if num < 0:
        return None

    # the empty row right below the diagram are also available (for +1)
    return sinf_multiply_e_recursive(lda, num, list(range(len(box_circle)+1)))

def sinf_multiply_e_recursive(lda, num, okrows):


    print(lda, num, okrows)
    # base case
    if num == 0:
        return [lda]
    if len(okrows) == 0:
        return []


    result = []
    count = 0

    # i is the row index, okrowsidx is i's location in okrows
    for okrowsidx,i in enumerate(okrows):
        # make copy so that original lda is not modified
        box_circle = list(lda[0])
        box_only = list(lda[1])
        # sufficient to consider the case where
        # all boxes later are added to rows below current box
        okrows_temp = okrows[okrowsidx+1:]


        # print("I am row", i)
        # edge case, can add to the empty row
        # only if the last non-empty row is not a circle
        if i == len(box_circle):
            if box_only[i-1] == 0:
                continue
            else:
                box_only += [1]
                box_circle += [1]
                # add the new empty row
                okrows_temp.append(i+1)
                count += 1
                print("child", count, "of", lda, "box added at", i)
                result += sinf_multiply_e_recursive([box_circle, box_only],
                            num-1, okrows_temp)


        # if box_only fails to be a partition after
        # insertion, skip this case
        if i != 0 and (box_only[i]+1) > box_only[i-1]:
            continue


        # a circle is in the row
        if (box_circle[i]-box_only[i]) == 1:
            box_only[i] += 1
            b_row = ball_target_row(box_circle, i)
            # print("I am row", i, "ball drop to", b_row)

            # circle collision (vertically), stop
            # check == since we know we will fall into b_row
            # so either a box or circle in b_row-1 stops us
            if (b_row != 0) and (box_only[b_row-1] == box_only[b_row]):
                continue
            else:
                box_circle[b_row] += 1


            count += 1
            print("child", count, "of", lda, "box added at", i)
            result += sinf_multiply_e_recursive([box_circle, box_only],
                        num-1, okrows_temp)
        # no circle is in the row
        else:
            box_only[i] += 1
            box_circle[i] += 1
            count += 1
            print("child", count, "of", lda, "box added at", i)
            result += sinf_multiply_e_recursive([box_circle, box_only],
                        num-1, okrows_temp)


    return result


def ball_target_row(box_circle, iniRow):

    # target column
    target_col = box_circle[iniRow]+1
    for i in range(iniRow-1, -1, -1):
        if box_circle[i] >= target_col:
            return i+1

    # two exceptional cases:
    # 1. the iniRow is already row 0
    # 2. all rows above have nothing in target column
    # in both cases, the ball falls into row 0
    return 0

print(sinf_multiply_e([[4,3,1,1,1],[3,2,1,1]],3))