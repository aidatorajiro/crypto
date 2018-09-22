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
        else:
            raise NotImplementedError("Quadratic residue for this prime is not implemented")

    def modinv(self, x):
        return pow(x, self.p - 2, self.p)

    def check(self, xyz):
        (x, y, z) = xyz
        return y**2*z % self.p == (x**3 + self.a*x*z**2 + self.b*z**3) % self.p

    def eq(self, p1, p2):
        (x1, y1, z1) = p1
        (x2, y2, z2) = p2
        return (x1*z2 % self.p == x2*z1 % self.p) and (y1*z2 % self.p == y2*z1 % self.p)

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

    def add(self, p1, p2):
        (x1, y1, z1) = p1
        (x2, y2, z2) = p2

        if z1 == 0:
            return p2

        if z2 == 0:
            return p1

        r = (y1 * z2 - y2 * z1)                         % self.p
        s = (x1 * z2 - x2 * z1)                         % self.p

        if s == 0:
            return self.dbl(p1)

        s2 = s**2                                       % self.p
        t = (z1 * z2 * r**2 - s2 * (x1 * z2 + x2 * z1)) % self.p
        u = z2 * s**2                                   % self.p
        x3 = t * s                                      % self.p
        y3 = (r * (x1 * u - t) - y1 * u * s)            % self.p
        z3 = z1 * u * s                                 % self.p

        return (x3, y3, z3)

    def scale(self, xyz, k):
        tmp = (0, 0, 0)
        while k != 0:
            if k & 1 == 1:
                tmp = self.add(tmp, xyz)
            k = k >> 1
            xyz = self.dbl(xyz)
        return tmp

    def toXY(self, xyz):
        x, y, z = xyz
        zinv = self.modinv(z)
        return (x*zinv % self.p, y*zinv % self.p)

E = Ell(0,7,2**256 - 0x1000003D1)
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8, 1)
n = 2**256 - 0x14551231950b75fc4402da1732fc9bebf
print("Is G on the curve?:", E.check(G))
print("Is 2G on the curve?:", E.check(E.dbl(G)))
print("Is 4G on the curve?:", E.check(E.dbl(E.dbl(G))))
print("2G as xy-coordinate:", E.toXY(E.dbl(G)))
print("4G as xy-coordinate:", E.toXY(E.dbl(E.dbl(G))))
print("12345G as xy-coordinate:", E.toXY(E.scale(G, 12345)))
# print(E.scale(G, n))
# print(E.scale(G, 10000))
