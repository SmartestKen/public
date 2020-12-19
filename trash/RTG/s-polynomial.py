#!/usr/bin/python3

print("using grlex")
print("f leading monomial x^3*y^2 (3,2)")
print("g leading monomial x^4*y (4,1)")
input("")
print("lcm, taking max exponent of each variable..")
print("x^4*y^2 (4,2)")
input("")
print("taking difference...")
print("f part ---> (x^4*y^2/(x^3*y^2))*f")
print("g part ---> -(x^4*y^2/(3*x^4*y))*g")

print("s polynomial")
print("-x^3*y^3 + x^2 - (1/3)*y^3")