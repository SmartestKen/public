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
input("")


print("using grlex")
print("iteration 1")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1}")
print("remaining pair (1,2)")

print("select S(1,2) = x")

print("division remainder = x")

print("updating...")

print("iteration 2")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1, x}")
print("remaining pair (1,3), (2,3)")

print("select S(2,3) = 2*y^3-1")

print("division remainder = 2*y^3-1")

print("updating...")

print("iteration 3")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1, x, 2*y^3-1}")
print("remaining pair (1,3), (1,4), (2,4), (3,4)")

print("select S(1,3) = 2*x*y^2")

print("division remainder = 0")

print("no need to update")

print("iteration 4")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1, x, 2*y^3-1}")
print("remaining pair (1,4), (2,4), (3,4)")

print("select S(1,4) = (1/2)*x^2 + 2*x*y^5")

print("division remainder = 0")

print("no need to update")




print("iteration 5")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1, x, 2*y^3-1}")
print("remaining pair (2,4), (3,4)")

print("select S(2,4) = (1/2)*x + 2*y^5 - y^2")

print("division remainder = 0")

print("no need to update")

print("iteration 6")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1, x, 2*y^3-1}")
print("remaining pair (3,4)")

print("select S(3,4) = (1/2)*x")

print("division remainder = 0")

print("no need to update")

print("---------------------------------------------")
print("grobner basis {x^2+2*x*y^2, x*y+2*y^3-1, x, 2*y^3-1}")
print("minimal grobner basis {x, 2*y^3-1}")