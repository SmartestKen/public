#!/usr/bin/python3
import time


print("using grlex")
print("iteration 1")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1}")
print("remaining pair (1,2)")

print("select S(1,2) = x")
time.sleep(1)
print("division remainder = x")

print("updating...")

input("")
print("iteration 2")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1, x}")
print("remaining pair (1,3), (2,3)")

print("select S(2,3) = 2*y^3-1")
time.sleep(1)
print("division remainder = 2*y^3-1")

print("updating...")

input("")
print("iteration 3")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1, x, 2*y^3-1}")
print("remaining pair (1,3), (1,4), (2,4), (3,4)")

print("select S(1,3) = 2*x*y^2")
time.sleep(0.3)
print("division remainder = 0")

print("no need to update")
input("")
print("iteration 4")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1, x, 2*y^3-1}")
print("remaining pair (1,4), (2,4), (3,4)")

print("select S(1,4) = (1/2)*x^2 + 2*x*y^5")
time.sleep(0.3)
print("division remainder = 0")

print("no need to update")

input("")


print("iteration 5")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1, x, 2*y^3-1}")
print("remaining pair (2,4), (3,4)")

print("select S(2,4) = (1/2)*x + 2*y^5 - y^2")
time.sleep(0.3)
print("division remainder = 0")

print("no need to update")
input("")
print("iteration 6")
print("generator set {x^2+2*x*y^2, x*y+2*y^3-1, x, 2*y^3-1}")
print("remaining pair (3,4)")

print("select S(3,4) = (1/2)*x")
time.sleep(0.3)
print("division remainder = 0")

print("no need to update")
input("")
print("---------------------------------------------")
print("grobner basis {x^2+2*x*y^2, x*y+2*y^3-1, x, 2*y^3-1}")
print("minimal grobner basis {x, 2*y^3-1}")