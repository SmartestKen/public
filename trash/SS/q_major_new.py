from sage.all import *

def f(lda, i):
    q = var('q')
    result = 0
    ST_list = StandardTableaux(lda).list();
    for ST in ST_list:
        ds = ST.standard_descents()
        # print(ds, result)
        if len(ds) == i:
            result += q**sum(ds)
    return result

def F(lda):
    q = var('q')
    t = var('t')
    d = sum(lda)
    result = 0
    ST_list = StandardTableaux(lda).list();
    for ST in ST_list:
        ds = ST.standard_descents()
        # sum(q^maj(T)*t^des(T))
        result += q**sum(ds)*t**len(ds)

    for i in range(0, d+1):
        result /= (1-q**i*t)

    return result


# N is the numerator of F
def N(lda):
    q = var('q')
    t = var('t')
    result = 0
    ST_list = StandardTableaux(lda).list();
    for ST in ST_list:
        ds = ST.standard_descents()
        # sum(q^maj(T)*t^des(T))
        result += q**sum(ds)*t**len(ds)

    return result


def phi(lda, mu):

    q = var('q')
    t = var('t')
    result = 0
    for k in range(0, sum(lda)-sum(mu)):
        result += q**int(k*(k+1)/2)*q_binomial(sum(lda)-sum(mu)-1,k)*(-q**sum(mu)*t)**(k+1)
    return result


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

        return subPartition(lda, curRow+1) + subPartition(mu2, curRow)






q = var('q')
t = var('t')

lda = [2,2]
mu_list = subPartition(lda, 0)
LHS = 0
RHS = 0


'''
# identity after removing blocks from tableau
for mu in mu_list:
    if mu == lda:
        LHS = (1-q**sum(lda)*t)*F(lda)
    else:
        RHS += q**sum(mu)*t*F(mu)
'''

'''
# after removing the denominators
for mu in mu_list:
    if mu == lda:
        LHS = N(lda)
    else:
        print("mu=", mu)
        temp_expr = 0
        for k in range(0, sum(lda)-sum(mu)):
            temp_expr += q**int(k*(k+1)/2)*q_binomial(sum(lda)-sum(mu)-1,k)*(-q**sum(mu)*t)**(k+1)
        RHS -= temp_expr*N(mu)
'''

# after taking derivative and collect terms
# i descent size
i = 1

for mu in mu_list:
    if mu == lda:
        LHS = f(lda, i)
        a = lda[0]
        k = lda[1]
        LHS2 = q**(i**2)*(q_binomial(a,i)*q_binomial(k,i)-q_binomial(a+1,i)*q_binomial(k-1,i))
        print("Part 1 ", q_binomial(a,i)*q_binomial(k,i))
        print("Part 2 ",-q_binomial(a+1,i)*q_binomial(k-1,i))
        print("--------------------------------------")

    else:
        for m in range(0, i+1):
            temp_expr = 0
            if (i-m) <= (sum(lda)-sum(mu)):
                temp_expr = q**int((i-m)*(i-m-1)/2)*q_binomial(sum(lda)-sum(mu)-1, i-m-1)*(-q**sum(mu))**(i-m)
                RHS -= temp_expr*f(mu, m)
                if f(mu,m) != 0 and temp_expr != 0:
                    print(mu, temp_expr, " and ", f(mu,m))


print("----------------------")
print(LHS.simplify_rational())
print(RHS.simplify_rational())
print((LHS - RHS).simplify_rational())
print((LHS / RHS).simplify_rational())