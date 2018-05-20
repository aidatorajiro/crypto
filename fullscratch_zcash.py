from collections import namedtuple
import hashlib
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

# substitute R to the line through P and Q.
def substitute(P, Q, R):
    if P == O:
        result = 1
    elif Q == O:
        result = 1
    elif Q == inv(P):
        result = R.x - P.x
    elif P == Q:
      result = P.x*(3*P.x**2+a) + (2*P.y)*R.y - (3*P.x**2 + a)*R.x - 2*P.y**2
    else:
      result = 
    
    return result

def miller(P, Q, l):
    f = 1
    V = P
    bs = format(l, 'b')[::-1]
    for i in bs:
        f = f**2 * subs_tang(V, Q) * inv_mod_p(subs_perp(add(V, V), Q))
        V = add(V, V)
        if i == 1:
            f = f * subs_tang(V, Q) * inv_mod_p(subs_perp(add(V, V), Q))
            V = add(V, P)
    assert V == mul(P, l) == O
    return f

# constants
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
p_plus_1_over_4 = (p + 1) // 4 # use for calculate sqrt(a) in F_p.
a = 0
b = 7
g = Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141 # order of the elliptic curve; mul(g, n) = O

