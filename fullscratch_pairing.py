from collections import namedtuple
import hashlib

Point = namedtuple("Point", "x y")
O = 'Origin'

def tocomp(obj):
    if type(obj) == int or type(obj) == Mod:
        return Complex(obj, 0)
    if type(obj) == Complex:
        return obj

class Complex(object):
    def __init__(self, r, i):
        self.r = r
        self.i = i

    def __mul__(self, other):
        k = tocomp(other)
        return Complex(self.r*k.r - self.i*k.i, self.r*k.i + self.i*k.r)

    def __rmul__(self, other):
        k = tocomp(other)
        return k * self

    def __add__(self, other):
        k = tocomp(other)
        return Complex(self.r + k.r, self.i + k.i)

    def __truediv__(self, other):
        k = tocomp(other)
        s = k.r**2 + k.i**2
        return Complex((self.r*k.r + self.i*k.i) / s, (self.i*k.r - self.r*k.i) / s)

    def __rtruediv__(self, other):
        k = tocomp(other)
        return k / self

    def __sub__(self, other):
        k = tocomp(other)
        return Complex(self.r - k.r, self.i - k.i)

    def __neg__(self):
        return Complex(-self.r, -self.i)

    def __pow__(self, n):
        bs = format(n, 'b')[::-1]
        tmp = self
        result = Complex(1, 0)
        for i in bs:
            if i == "1":
                result = result * tmp
            tmp = tmp*tmp
        return result

    def __eq__(self, other):
        k = tocomp(other)
        return self.r == k.r and self.i == k.i
    
    def __repr__(self):
        return str(self.r) + " + " + str(self.i) + "i"

def tomod(obj, p):
    if type(obj) == Mod:
        return Mod(obj.n, p)
    if type(obj) == int:
        return Mod(obj, p)

class Mod(object):
    def __init__(self, n, p):
        self.n = n % p
        self.p = p

    def __mul__(self, other):
        k = tomod(other, self.p)
        return Mod(self.n * k.n, self.p)

    def __rmul__(self, other):
        k = tomod(other, self.p)
        return k * self

    def __add__(self, other):
        k = tomod(other, self.p)
        return Mod(self.n + k.n, self.p)
    
    def __radd__(self, other):
        k = tomod(other, self.p)
        return k + self

    def __truediv__(self, other):
        k = tomod(other, self.p)
        return Mod(self.n * pow(k.n, p - 2, self.p), self.p)
    
    def __rtruediv__(self, other):
        k = tomod(other, self.p)
        return k / self

    def __sub__(self, other):
        k = tomod(other, self.p)
        return Mod(self.n - k.n, self.p)
    
    def __rsub__(self, other):
        k = tomod(other, self.p)
        return k - self

    def __neg__(self):
        return Mod(-self.n, self.p)

    def __pow__(self, k):
        return Mod(pow(self.n, k, self.p), self.p)

    def __eq__(self, other):
        k = tomod(other, self.p)
        return self.n % self.p == k.n % self.p

    def __repr__(self):
        return str(self.n % self.p) + " % " + str(self.p)

class Curve:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def valid(self, P):
        if P == O:
            return True
        else:
            return (P.y**2 - (P.x**3 + self.a*P.x + self.b)) == 0
    
    def inv(self, P):
        if P == O:
            return P
        return Point(P.x, -P.y)
    
    def add(self, P, Q):
        if not (self.valid(P) and self.valid(Q)):
            raise ValueError("Invalid inputs")

        # Deal with the special cases where either P, Q, or P + Q is
        # the origin.
        if P == O:
            result = Q
        elif Q == O:
            result = P
        elif Q == self.inv(P):
            result = O
        else:
            # Cases not involving the origin.
            if P == Q:
                dydx = (3 * P.x**2 + self.a) / (2 * P.y)
            else:
                dydx = (Q.y - P.y) / (Q.x - P.x)
            x = dydx**2 - P.x - Q.x
            y = dydx * (P.x - x) - P.y
            result = Point(x, y)

        assert self.valid(result)
        return result

    def mul(self, P, n):
        bs = format(n, 'b')[::-1]
        tmp = P
        result = O
        for i in bs:
            if i == "1":
                result = self.add(result, tmp)
            tmp = self.add(tmp, tmp)
        return result

    def miller(self, P, Q, l):
        def g(P1, P2, P3):
            if self.inv(P1) == P2:
                return P3.x - P1.x
            if P1 == P2:
                lam = (3*P1.x + self.a)/(2*P1.y)
            else:
                lam = (P2.y - P1.y)/(P2.x - P1.x)
            return P3.y - lam*(P3.x - P1.x) - P1.y
        f = 1
        V = P
        bs = format(l, 'b')[1:]
        for i in bs:
            V_dbl = self.add(V, V)
            f = (f*f*g(V, V, Q))/(g(V_dbl, self.inv(V_dbl), Q))
            V = self.add(V, V)
            if i == '1':
                f = f*(g(V, P, Q))/(g(self.add(V, P), self.inv(self.add(V, P)), Q))
                V = self.add(V, P)
        assert V == self.mul(P, l)
        return f

p = 0x30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47

E = Curve(Complex(Mod(0, p), Mod(0, p)), 3/Complex(Mod(9, p), Mod(1, p)))
P = Point(
        Complex(
            Mod(0x1800deef121f1e76426a00665e5c4479674322d4f75edadd46debd5cd992f6ed, p),
            Mod(0x198e9393920d483a7260bfb731fb5d25f1aa493335a9e71297e485b7aef312c2, p)),
        Complex(
            Mod(0x12c85ea5db8c6deb4aab71808dcb408fe3d1e7690c43d37b4ce6cc0166fa7daa, p), 
            Mod(0x090689d0585ff075ec9e99ad690c3395bc4b313370b38ef355acdadcd122975b, p)))

X = E.mul(P, 10000)
Y = E.mul(P, 50000)
Z = E.mul(P, 50000*10000)

print(E.valid(P))
print(E.valid(X))
print(E.valid(Y))
print(E.miller(X, Y, 1234567))
print(E.miller(Z, P, 1234567))