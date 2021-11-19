# fullscratch weil pairing

from collections import namedtuple
import hashlib

Point = namedtuple("Point", "x y")
O = 'Origin'

def ext_euc(a, b):
    e1 = 0
    f1 = 0
    c = a // b
    d = a - c*b
    e2 = 1
    f2 = -1*c
    if d == 0:
        return (a, b, c, d, e1, f1, e2, f2, 0, 0)
    a = b
    b = d
    c = a // b
    d = a - c*b
    e3 = -1*c*e2
    f3 = 1-c*f2
    if d == 0:
        return (a, b, c, d, e1, f1, e2, f2, e3, f3)
    while True:
        a = b
        b = d
        c = a // b
        d = a - c*b
        e1 = e2
        f1 = f2
        e2 = e3
        f2 = f3
        e3 = e1 - c*e2
        f3 = f1 - c*f2
        if d == 0:
            break
    return (a, b, c, d, e1, f1, e2, f2, e3, f3)

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
        if k.n == 1:
            return self
        return Mod((self.n * ext_euc(self.p, k.n) [7]) % self.p, self.p)
    
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
                dydx = (3 * P.x ** 2 + self.a) / (2 * P.y)
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
        def g(P1, P2):
            if self.inv(P1) == P2:
                if P1 == "Origin":
                    return 1  # div f = 3(O) - 3(O) = 0 → f = non-zero const .
                return Q.x - P1.x
            if P1 == P2:
                if P1 == "Origin":
                    return 1 # div f = 3(O) - 3(O) = 0 → f = non-zero const .
                lam = (3 * P1.x ** 2 + self.a)/(2 * P1.y)
            else:
                if P1 == "Origin":
                    raise NotImplementedError("wakaran") # div f = (P2) - (O) → ???
                if P2 == "Origin":
                    raise NotImplementedError("wakaran") # div f = (P1) - (O) → ???
                lam = (P2.y - P1.y)/(P2.x - P1.x)
            P3 = self.add(P1, P2)
            return (Q.y - lam*(Q.x - P1.x) - P1.y)/(Q.x - P3.x)
        f = 1
        V = P
        bs = format(l, 'b')[1:]
        for i in bs:
            f = f*f*g(V, V)
            V = self.add(V, V)
            if i == '1':
                f = f*g(V, P)
                V = self.add(V, P)
        assert V == 'Origin'
        return f

if __name__ == "__main__":
    p = 1047105072135367943  # a prime s.t. p % 12 == 11, and sqrt(2) exists in F_p, and p - 1 has a big prime factor
    
    E1 = Curve(Complex(Mod(0, p), Mod(0, p)), Complex(Mod(3, p), Mod(0, p)))
    P1 = Point(Complex(Mod(1, p), Mod(0, p)), Complex(Mod(2, p), Mod(0, p)))
    
    sqex = (p + 1) // 4
    
    sq2 = Complex(Mod(2, p), Mod(0, p)) ** sqex
    assert sq2 ** 2 == Complex(Mod(2, p), Mod(0, p))
    
    def mkp(k):
        A = Mod(k, p)
        B = ( (A**3 + 3)/(3 * A) ) ** sqex
        assert B**2 == (A**3 + 3)/(3 * A)
        X = Complex(A, B)
        sqi = sq2 / 2 + sq2 / 2 * Complex(Mod(0, p), Mod(1, p))
        assert (((X**3 + 3).i)**sqex)**2 == (X**3 + 3).i
        Y = sqi * ((X**3 + 3).i)**sqex
        assert (Y**2 == X**3 + 3)
        
        return Point(X, Y)
    
    P2 = mkp(6)
    
    r = 1339334197
    
    P11 = E1.mul(P1, 218627*149*2*2*2)
    
    # common order for all points
    l = p + 1
    assert E1.mul(P11, r) == "Origin"
    assert E1.mul(P2, l) == "Origin"
    
    assert (p**2 - 1) % r == 0
    
    # weil pairing
    w = lambda X, Y: E1.miller(X, Y, l)**((p**2 - 1)//r)
    
    def pt(i, j):
        print(str(i) + ", " + str(j))
        print(w(E1.mul(P1, i), E1.mul(P2, j)))
    
    pt(1,1)
    pt(1,2)
    pt(1,3)
    pt(1,4)
    pt(10,10)
    pt(100,1)
    pt(1,100)
