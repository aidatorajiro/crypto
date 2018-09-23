import random

class Ell:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        if p % 4 == 3:
            self.p14 = (p+1)//4

    """
    Calculate a quardratic rasidue for given integer in F_p.
    """
    def modsqrt(self, x):
        if p % 4 == 3:
            return math.pow(x, self.p14, self.p)
        else:
            raise NotImplementedError("Quadratic residue for this prime is not implemented")

    """
    Calculate modulo inverse for given integer in F_p.
    """
    def modinv(self, x):
        return pow(x, self.p - 2, self.p)

    """
    Return if given coordinate is on the curve.
    """
    def check(self, xyz):
        (x, y, z) = xyz
        return y**2*z % self.p == (x**3 + self.a*x*z**2 + self.b*z**3) % self.p

    """
    Return if p1 is equals to p2.
    """
    def eq(self, p1, p2):
        (x1, y1, z1) = p1
        (x2, y2, z2) = p2
        return ((x1*z2 - x2*z1) % self.p == 0) and ((y1*z2 - y2*z1) % self.p == 0)
    """
    Return if p1 is inverse of p2.
    """
    def isInv(self, p1, p2):
        (x1, y1, z1) = p1
        (x2, y2, z2) = p2
        return ((x1*z2 - x2*z1) % self.p == 0) and ((y1*z2 - y2*z1) % self.p != 0)

    """
    Return inverse of given point.
    """
    def inv(self, p):
        return (p[0], (-p[1]) % self.p, p[2])

    """
    Double given point.
    """
    def dbl(self, xyz):
        (x, y, z) = xyz

        if z == 0:
            return xyz

        r = (3 * x**2 + self.a * z**2)     % self.p
        s = 2 * y * z                      % self.p
        s2 = s**2                          % self.p
        s3 = s2 * s                        % self.p
        t = y**2 * z                       % self.p
        xt = x * t                         % self.p
        u = (r**2 - 8 * xt)                % self.p
        x2 = u * s                         % self.p
        y2 = (r * (4 * xt - u) - 8 * t**2) % self.p

        return (x2, y2, s3)

    """
    Add given two points.
    """
    def add(self, p1, p2):
        (x1, y1, z1) = p1
        (x2, y2, z2) = p2

        if z1 == 0:
            return p2

        if z2 == 0:
            return p1

        r = (y1 * z2 - y2 * z1)                         % self.p
        s = (x1 * z2 - x2 * z1)                         % self.p

        if s == 0 and r == 0:
            return self.dbl(p1)

        s2 = s**2                                       % self.p
        t = (z1 * z2 * r**2 - s2 * (x1 * z2 + x2 * z1)) % self.p
        u = z2 * s**2                                   % self.p
        x3 = t * s                                      % self.p
        y3 = (r * (x1 * u - t) - y1 * u * s)            % self.p
        z3 = z1 * u * s                                 % self.p

        return (x3, y3, z3)

    """
    Scale given point by integer k.
    """
    def scale(self, xyz, k):
        tmp = (0, 0, 0)
        while k != 0:
            if k & 1 == 1:
                tmp = self.add(tmp, xyz)
            k = k >> 1
            xyz = self.dbl(xyz)
        return tmp

    """
    Convert given point to xy-coordinate. If z == 0, returns "Origin".
    (x, y, z) |-> (x / z, y / z)
    """
    def toXY(self, xyz):
        x, y, z = xyz
        if z % self.p == 0:
            return "Origin"
        zinv = self.modinv(z)
        return (x*zinv % self.p, y*zinv % self.p)

    """
    Calculate the equation of tangent line of p, then substitute q to it.
    """
    def getTangentLine(self, p, q):
        (x1, y1, z1) = p
        (x2, y2, z2) = q

        r = (3 * x1**2 + self.a * z1**2)
        s = 2 * y1 * z1

        return ((y2 * z1 * s - y1 * z2 * s + x1 * z2 * r - x2 * z1 * r) % self.p, z1 * z2 * s % self.p)

    """
    Calculate the equation of vertical line of p, then substitute q to it.
    """
    def getVerticalLine(self, p, q):
        (x1, y1, z1) = p
        (x2, y2, z2) = q
        return ((x2 * z1 - x1 * z2) % self.p, z1 * z2 % self.p)

    """
    Calculate the equation of line between p and q, then substitute r to it.
    """
    def getLine(self, p, q, r):
        (x1, y1, z1) = p
        (x2, y2, z2) = q
        (x3, y3, z3) = r

        if z1 == 0:
            return ((x2 * y3 - x3 * y2), x2 * z3 % self.p)

        if z2 == 0:
            return ((x1 * y3 - x3 * y1), x1 * z3 % self.p)

        if self.eq(p, q):
            return self.getTangentLine(p, r)

        if self.isInv(p, q):
            return self.getVerticalLine(p, r)

        r = (y1 * z2 - y2 * z1)                         % self.p
        s = (x1 * z2 - x2 * z1)                         % self.p
        return ((y3 * z1 * s - y1 * z3 * s + x1 * z3 * r - x3 * z1 * r) % self.p, z1 * z3 * s % self.p)

    """
    Calculate Tate pairing using Miller's Algotithm
    """
    def tate(self, p, q, k):
        f = 1
        fz = 1
        v = p

        for i in format(k, "b")[1:]:
            (x, xz) = self.getTangentLine(v, q)
            v = self.dbl(v)
            (y, yz) = self.getVerticalLine(v, q)

            f = (f**2 * x * yz) % self.p
            fz = (fz**2 * xz * y) % self.p

            if i == "1":
                (x, xz) = self.getLine(v, p, q)
                v = self.add(v, p)
                (y, yz) = self.getVerticalLine(v, q)

                f = (f * x * yz) % self.p
                fz = (fz * xz * y) % self.p

        print(v)

        return (f, fz)

E = Ell(0,7,2**256 - 0x1000003D1)
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8, 1)
n = 2**256 - 0x14551231950b75fc4402da1732fc9bebf

G1 = E.scale(G, 10000)
G3 = E.scale(G, 30000)
G4 = E.scale(G, 40000)

print("Is G on the curve?:", E.check(G))
print("Is 2G on the curve?:", E.check(E.dbl(G)))
print("Is 4G on the curve?:", E.check(E.dbl(E.dbl(G))))
print("2G as xy-coordinate:", E.toXY(E.dbl(G)))
print("4G as xy-coordinate:", E.toXY(E.dbl(E.dbl(G))))
print("10000G as xy-coordinate:", E.toXY(G1))
print("10000G + 30000G == 40000G?:", E.eq(E.add(G1, G3), G4))
print("nG:", E.scale(G1, n))
print("Multiply by random 256-bit integer:", E.scale(G, random.randint(0, 2**256)))
print("isInv(P, inv(P)):", E.isInv(G3, E.inv(G3)))
print("GetLine(P, Q, P):", E.getLine(G1, G3, G1))
print("GetLine(P, Q, Q):", E.getLine(G1, G3, G3))
print("GetLine(P, Q, -(P + Q)):", E.getLine(G1, G3, E.inv(G4)))
print("GetTangentLine(P, -2P):", E.getTangentLine(G1, E.inv(E.dbl(G1))))

val = lambda x: x[0]*E.modinv(x[1])%E.p
print("e(G, G)", E.tate(G, G, n))
print("e(1000G, 7777G)", val(E.tate(E.scale(G, 1000), E.scale(G, 7777), n)))
print("e(10G, 1111G)^700", pow(val(E.tate(E.scale(G, 10), E.scale(G, 1111), n)), 700, E.p))
# print(E.scale(G, n))
# print(E.scale(G, 10000))
