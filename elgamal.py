import random
import math

p = 23
g = 5
x = 6
H = 15

y = pow(g, x, p)

while True:
    k = random.randint(2, p - 2)
    if math.gcd(k, p - 1) == 1:
        break

r = pow(g, k, p)
k_inv = pow(k, -1, p - 1)
s = (k_inv * (H - x * r)) % (p - 1)

v1 = pow(g, H, p)
v2 = (pow(y, r, p) * pow(r, s, p)) % p

print("Public Key =", y)
print("Private Key =", x)
print("k =", k)
print("r =", r)
print("s =", s)

if v1 == v2:
    print("Signature is VALID")
else:
    print("Signature is INVALID")