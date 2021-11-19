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
        return Mod(self.n * pow(k.n, self.p - 2, self.p), self.p)
    
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
        def g(P1, P2):
            if P1 == 'Origin':
                return 1
            if self.inv(P1) == P2:
                return Q.x - P1.x
            if P1 == P2:
                lam = (3*P1.x + self.a)/(2*P1.y)
            else:
                lam = (P2.y - P1.y)/(P2.x - P1.x)
            return (Q.y - lam*(Q.x - P1.x) - P1.y)/(Q.x + P1.x + P2.x - lam * lam)
        
        V = P
        f = 1
        bs = format(l, 'b')[1:]
        for i in bs:
            f = f * f * g(V, V)
            V = self.add(V, V)
            if i == '1':
                f = f * g(V, P)
                V = self.add(V, P)
        assert V == self.mul(P, l)
        assert V == 'Origin'
        return f

if __name__ == "__main__":
    p = 24048719

    E = Curve(Mod(2, p), Mod(3, p))
    
    P1 = Point(Mod(17334095, p), Mod(5644719, p))
    
    P2 = Point(Mod(10356700, p), Mod(18392425, p))
    
    P3 = Point(Mod(19785863, p), Mod(21314362, p))
    
    print(E.valid(P1))
    print(E.valid(P2))
    
    """
    PP = 'Origin'
    
    for i in range(p**2):
        PP = E.add(PP, P)
        if PP == 'Origin':
            r = i + 1
            break
    
    def ssqq(x, y):
        return math.sqrt((math.sqrt(x**2+y**2)+x)/2)
    
    list(filter(lambda S: S[0].is_integer(), map(lambda R: [ssqq(R.r, R.i), R], [Complex(x,y)**3 + Complex(x,y)*Complex(13, 19)/2 + Complex(19, 23) for x in range(3, 10) for y in range(3, 10)])))
    
    Q = Point(
        Complex(
            Mod(, p),
            Mod(, p)),
        Complex(
            Mod(, p), 
            Mod(, p)))
    """

    #X = E1.mul(P1, 10000)
    #Y = E2.mul(P2, 50000)

    # two prime orders
    l1 = 7933
    l2 = 379
    l3 = 7933*379

    # check order
    print(E.mul(P1, l1))
    print(E.mul(P2, l2))

    print(E.miller(E.mul(P2,10), E.mul(P1,10), l2))
    print(E.miller(E.mul(P2,100), E.mul(P1,1), l2))
    
    def w(X, Y):
        Z = P3
        l = l3
        return (E.miller(X, E.add(Y, Z), l) / E.miller(X, Z, l)) / (E.miller(Y, E.add(X, E.inv(Z)), l) / E.miller(Y, E.inv(Z), l))

    def t(X, Y):
        Z = P2
        l = l1
        return (E.miller(X, E.add(Y, Z), l) / E.miller(X, Z, l))**((l - 1)//3)

    print(w(E.mul(P1, 10), E.mul(P2, 10)))
    print(w(E.mul(P1, 100), E.mul(P2, 1)))
    print(w(E.mul(P1, 1), E.mul(P2, 100)))
    print(w(E.mul(P1, 1), E.mul(P2, 1)))
    print(w(E.mul(P1, 1), E.mul(P2, 1))**100)
    print(w(E.add(E.mul(P1, 10), E.mul(P1, 20)), E.mul(P2, 30)))
    print(w(E.mul(P1, 10), E.mul(P2, 30)) + w(E.mul(P1, 20), E.mul(P2, 30)))
    print(w(E.mul(P1, 3), E.mul(P1, 4)))
    print(w(E.mul(P1, 1), E.mul(P1, 1))**12)
    print(t(E.add(E.mul(P1, 10), E.mul(P1, 20)), E.mul(P1, 30)))
    print(t(E.mul(P1, 10), E.mul(P1, 30))*t(E.mul(P1, 20), E.mul(P1, 30)))

    #print(w(E1.mul(P1, 1), E2.mul(P2, 1)))

    #print(e(X, Y))
    #print(e(Z, W))
