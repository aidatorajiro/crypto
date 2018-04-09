from collections import namedtuple
Point = namedtuple("Point", "x y")

O = 'Origin'

import random
import time

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
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141 # order of the elliptic curve; mul(g, n) = O

while True:
    # generate private key
    priv = random.randint(1, n - 1)
    
    # generate public key
    pub = mul(g, priv)
    
    # sign
    m = random.randint(1, n - 1) # message hash
    k = random.randint(1, n - 1)
    kg = mul(g, k)
    r = kg.x % n
    s = pow(k, n-2, n)*(m + r*priv) % n
    
    # verify
    assert pub != O
    assert valid(pub)
    assert mul(pub, n) == O
    assert 1 <= r <= n - 1
    assert 1 <= s <= n - 1
    assert r == add(mul(g, pow(s, n-2, n)*m), mul(pub, pow(s, n-2, n)*r)).x
    
    time.sleep(1)