from sage.all import *
# toggle = true, get par larger than ref
# toggle = false, get par smaller than ref
def getIP(n, par, ref, toggle):

    if len(par) == 0:
        max = n
    else:
        if toggle and (sum(par) < sum(ref[:len(par)])):
            return []
        if not toggle and (sum(par) > sum(ref[:len(par)])):
            return []

        if n == 0:
            return [par]

        if n > par[-1]:
            max = par[-1]
        else:
            max = n

    result = []
    for i in range(1, max+1):
        temp_par = list(par)
        temp_par.append(i)
        result += getIP(n-i, temp_par, ref, toggle)
    return result

Sym = SymmetricFunctions(QQ)
h = Sym.homogeneous()
e = Sym.elementary()
m = Sym.monomial()
s = Sym.schur()
s(h([2,1]))