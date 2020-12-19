# input [box_circle, box_only] output [lda_a, lda_s]
def bc_to_row(lda):

    box_circle = lda[0]
    box_only = lda[1]
    box_only += [0]*(len(box_circle)-len(box_only))
    lda_a = []
    lda_s = []

    for i in range(len(box_circle)):
        if box_circle[i] != box_only[i]:
            lda_a.append(box_only[i])
        else:
            lda_s.append(box_only[i])
    return [lda_a, lda_s]


# input [lda_a, lda_s] output [box_circle, box_only]
def row_to_bc(lda):
    lda_a = lda[0]
    lda_s = lda[1]
    box_circle = sorted([x+1 for x in lda_a] + lda_s, reverse=True)
    box_only = sorted(lda_a + lda_s, reverse=True)
    print(box_circle)
    return [box_circle, box_only]


