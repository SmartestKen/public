'''
LHS = 0
RHS = 0
LHS = q**3*t+q**2*t+q*t
RHS += (q**2*t+q*t)*(q**3*t)
RHS += q*t*(q**2*t)*(1-q**3*t)
RHS += q**3*t
RHS += q**2*t*(1-q**3*t)
RHS += q*t*(1-q**2*t)*(1-q**3*t)
print(LHS.simplify_rational())
print(RHS.simplify_rational())
print((LHS - RHS).simplify_rational())
print((LHS / RHS).simplify_rational())
'''