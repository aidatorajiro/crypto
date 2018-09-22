import math

class Ell:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        if p % 4 == 3:
            self.p14 = (p+1)//4
    def modsqrt(self, x):
        if p % 4 == 3:
            return math.pow(x, self.p14, self.p)
    def modinv(self, x):
        return math.pow(x, p - 2, p)
    def check(self, xyz):
        (x, y, z) = xyz
        return y**2*z % self.p == (x**3 + self.a*x*z**2 + self.b*z**3) % self.p
    def eq(self, p1, p2):
        (x1, y1, z1) = p1
        (x2, y2, z2) = p2
        return (x1*z2 % self.p == x2*z1 % self.p) and (y1*z2 % self.p == y2*z1 % self.p)
    def dbl(self, xyz):
        (x, y, z) = xyz
        r = (3*x**2 + self.a*z**2) % self.p
        s = 2*y*z % self.p
        t = x*s**2 % self.p
        u = (r**2 - 2*t) % self.p
        s3 = s**3 % self.p
        return (s*u % self.p, (r*(u - t) + y*s3) % self.p, s3)
    def add(self, p1, p2):
        (x1, y1, z1) = p1
        (x2, y2, z2) = p2
        
    def scale(self, xyz, k):
        tmp = xyz
        while k != 0:
            if k & 1 == 1:
                xyz = self.add(tmp, xyz)
            k = k >> 1
            tmp = self.dbl(tmp)
        return xyz

E = Ell(0,7,2**256 - 0x1000003D1)
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8, 1)
print(E.check(E.dbl(G)))
print(E.scale(G, 10000))