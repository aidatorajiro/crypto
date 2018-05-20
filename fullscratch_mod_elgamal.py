from collections import namedtuple
Point = namedtuple("Point", "x y")

O = 'Origin'

import random

def sqrt_mod_p(n):
    sqn = pow(n, p_plus_1_over_4, p)
    assert sqn**2%p == n
    return sqn

def int_to_point(n):
    x = n
    y = sqrt_mod_p(x**3 + a*x + b)
    P = Point(x, y)
    assert valid(P)
    return P

def valid(P):
    if P == O:
        return True
    else:
        return (
            (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and
            0 <= P.x < p and 0 <= P.y < p)

def inv_mod_p(x):
    if x % p == 0:
        raise ZeroDivisionError("Impossible inverse")
    return pow(x, p-2, p)

def inv(P):
    if P == O:
        return P
    return Point(P.x, (-P.y)%p)

def add(P, Q):
    if not (valid(P) and valid(Q)):
        raise ValueError("Invalid inputs")

    # Deal with the special cases where either P, Q, or P + Q is
    # the origin.
    if P == O:
        result = Q
    elif Q == O:
        result = P
    elif Q == inv(P):
        result = O
    else:
        # Cases not involving the origin.
        if P == Q:
            dydx = (3 * P.x**2 + a) * inv_mod_p(2 * P.y)
        else:
            dydx = (Q.y - P.y) * inv_mod_p(Q.x - P.x)
        x = (dydx**2 - P.x - Q.x) % p
        y = (dydx * (P.x - x) - P.y) % p
        result = Point(x, y)
    
    assert valid(result)
    return result

def mul(P, n):
  bs = format(n, 'b')[::-1]
  tmp = P
  result = O
  for i in bs:
    if i == "1":
      result = add(result, tmp)
    tmp = add(tmp, tmp)
  return result

# constants
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
p_plus_1_over_4 = (p + 1) // 4 # use for calculate sqrt(a) in F_p.
a = 0
b = 7
g = Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
h = Point(0x9d5e157c5f8d4c57411a6188f28562ec5b1c6834c94e750440cde368b22f6cc0, 0x429d6b3c408d76199a061d2b5e7211e6ea0466225d0403599a0f96840002bc1a)
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141 # order of the elliptic curve; mul(g, n) = O

# generate private key
#priv = random.randint(1, n - 1)
priv = 0x4545e45bae6aed7e1661208d5fb57473f4902b0cfe365de7f72eab60db999cda

# generate public key
pub = mul(g, priv)

# encrypt
r1 = 0x78f5c26b8059a0a3690de4d258caa4e6a5f09eb21e708c2bf75616f62d9e7d14
m1 = 100000000000000000
c1 = (mul(g, r1), add(mul(pub, r1), mul(h, m1)))

r2 = 0x62c193c3ea21c147f18bbd1250a7d98355c7e10ea172e518797be8d409a03f9f
m2 = 200000000000000000
c2 = (mul(g, r2), add(mul(pub, r2), mul(h, m2)))

c12 = (add(c1[0], c2[0]), add(c1[1], c2[1]))

# decrypt
