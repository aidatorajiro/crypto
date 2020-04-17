# Statistics (and a little cryptography) over a finite field - fullscratch version
# composite multiple base keys to a single masterkey using polynomial fitting
# the masterkey cannot be computed without having at least k base keys
# the masterkey can ganerate base keys
# use numpy to run this script

def tomod(obj, p):
    if type(obj) == Mod:
        return Mod(obj.n, p)
    if type(obj) == int:
        return Mod(obj, p)
    if type(obj) == float:
        return Mod(int(obj), p)

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
        return Mod(self.n * ext_euc(k.n, self.p)[0], self.p)
    
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
        return "(" + str(self.n % self.p) + " % " + str(self.p) + ")"

def tovec(x):
    if type(x) == Vec:
        return x
    if type(x) == list:
        return Vec(x)
    raise Exception("invalid argument")

def mat_identity(n, x=1):
    l = [0]*(n*n)
    mat = Mat(l, n, n)
    for i in range(n):
        mat.modify(i, i, x)
    return mat

def mat_add(a, b):
    if type(a) == Vec and type(b) == Vec and a.n == b.n:
        return Vec([a.d[i] + b.d[i] for i in range(a.n)])
    if type(a) == Mat and type(b) == Mat and a.n == b.n and a.m == b.m:
        return Mat([a.d[i] + b.d[i] for i in range(a.n*a.m)], a.n, a.m)
    raise Exception("invalid argument")

def mat_dot(a, b):
    if type(a) == Vec and type(b) == Vec and a.n == b.n:
        return sum([a.d[i] * b.d[i] for i in range(a.n)])
    if type(a) == Mat and type(b) == Vec and a.m == b.n:
        bb = Mat(b.d, b.n, 1)
        return mat_dot(a, bb)
    if type(a) == Mat and type(b) == Mat and a.m == b.n:
        l = []
        for i in range(a.n):
            for j in range(b.m):
                l.append(a.getrow(i)*b.getcol(j))
        return Mat(l, a.n, b.m)
    raise Exception("invalid argument")

# destructive function to perform a gaussian reduction
# mats is a list of matrices
# if you set method == 'down', it will perform downward reduction and mats[0] will be upper triangular matrix
# if you set method == 'up', it will perform upward reduction and mats[0] will be lower triangular matrix
# matrices in mats other than mats[0] will follow reduction of mats[0]
def reduction(mats, method):
    n = mats[0].n
    if method == 'down':
        inds_1 = range(0, n - 1)
    elif method == 'up':
        inds_1 = range(n - 1, 0, -1)
    else:
        raise Exception("invalid argument")
    for i in inds_1:
        if method == 'down':
            inds_2 = range(i + 1, n)
        if method == 'up':
            inds_2 = range(i - 1, -1, -1)
        edge_i = mats[0].pos(i, i)
        for j in inds_2:
            edge_j = mats[0].pos(j, i)
            coeff = -(edge_j/edge_i)
            for mat in mats:
                mat.add_row_vec(j, mat.getrow(i).__mul__(coeff))

# scale each rows in mats so that mats[0] will be an identity matrix.
def reduction_scale(mats):
    for i in range(mats[0].n):
        scale = 1/mats[0].pos(i, i)
        for mat in mats:
            mat.mul_row_with(i, scale)

# use gaussian reduction to calculate an inverse matrix
def dotinv(mat):
    mat = mat.copy()
    out = mat_identity(mat.n)
    mats = [mat, out]
    reduction(mats, 'down')
    reduction(mats, 'up')
    reduction_scale(mats)
    return out

# make vandermonde matrix with shape (k, k) and parameters x
def vander(x, k):
    out = Mat([0]*(k*k), k, k)
    tmp = Vec([1]*k)
    for j in range(k-1, -1, -1):
        for i in range(k):
            out.modify(i, j, tmp.d[i])
        for i in range(k):
            tmp.d[i] *= x.d[i]
    return out

class Mat(object):
    def __init__(self, d, n, m):
        assert len(d) == n*m
        self.d = d
        self.n = n
        self.m = m
    def getrow(self, i):
        assert i < self.n
        return Vec(self.d[i*self.m:(i + 1)*self.m])
    def getcol(self, i):
        assert i < self.m
        return Vec([self.d[t] for t in range(i, self.n*self.m, self.m)])
    # get value at position (row = x, column = y)
    def pos(self, x, y):
        return self.d[x*self.m + y]
    # change position (row = x, column = y) to v
    def modify(self, x, y, v):
        self.d[x*self.m + y] = v
    # add specified row vector to specified row index
    def add_row_vec(self, i, v):
        assert v.n == self.m
        for j in range(v.n):
            self.d[i*self.m + j] += v.d[j]
    # multiple specified row with specified scalar
    def mul_row_with(self, i, v):
        for j in range(self.n):
            self.d[i*self.m + j] *= v
    def copy(self):
        return Mat(self.d.copy(), self.n, self.m)
    # destructive map function
    def map_dest(self, f):
        for i in range(self.n*self.m):
            self.d[i] = f(self.d[i])
        return self
    def map(self, f):
        return Mat(list(map(f, self.d)), self.n, self.m)
    def __add__(self, other):
        return mat_add(self, other)
    def __radd__(self, other):
        return mat_add(other, self)
    def __mul__(self, other):
        # self is left, other is right
        return mat_dot(self, other)
    def __rmul__(self, other):
        # self is right, other is left
        return mat_dot(other, self)
    def __neg__(self):
        return Mat(list(map(lambda x: -x, self.d)), self.n, self.m)
    def __repr__(self):
        s = "\n"
        for i in range(self.n):
            s += "[ "
            for j in range(self.m):
                s += str(self.pos(i, j)) + " "
            s += "]\n"
        return s
    def __eq__(self, other):
        return self.d == other.d and self.n == other.n and self.m == other.m

class Vec(object):
    def __init__(self, d):
        self.d = d
        self.n = len(d)
    def pos(self, x):
        return self.d[x]
    def copy(self):
        return Vec(self.d.copy())
    # destructive map function
    def map_dest(self, f):
        for i in range(self.n):
            self.d[i] = f(self.d[i])
        return self
    def map(self, f):
        return Vec(list(map(f, self.d)))
    def __add__(self, other):
        other = tovec(other)
        return mat_add(self, other)
    def __radd__(self, other):
        other = tovec(other)
        return mat_add(other, self)
    def __mul__(self, other):
        # self is left, other is right
        if type(other) == list or type(other) == Vec:
            other = tovec(other)
            return mat_dot(self, other)
        else:
            return self.map(lambda x: x*other)
    def __rmul__(self, other):
        # self is right, other is left
        if type(other) == list or type(other) == Vec:
            other = tovec(other)
            return mat_dot(other, self)
        else:
            return self.map(lambda x: other*x)
    def __truediv__(self, other):
        if type(other) == list or type(other) == Vec:
            pass
        else:
            return self.map(lambda x: x/other)
    def __rtruediv__(self, other):
        if type(other) == list or type(other) == Vec:
            pass
        else:
            return self.map(lambda x: other/x)
    def __repr__(self):
        return str(self.d)
    def __neg__(self):
        return Vec(list(map(lambda x: -x, self.d)))
    def __eq__(self, other):
        if type(other) == list:
            return self.d == other
        if type(other) == Vec:
            return self.d == other.d and self.n == other.n

# extended euclidean algorithm
def ext_euc(a1, b1):
    a = a1
    b = b1
    c = 0
    d = 0
    
    coeff_a_a1 = 1
    coeff_a_b1 = 0
    coeff_b_a1 = 0
    coeff_b_b1 = 1
    
    while True:
        c = a // b
        d = a % b
        if d == 0:
            return [coeff_b_a1, coeff_b_b1]
        coeff_a_a1_n = coeff_b_a1
        coeff_a_b1_n = coeff_b_b1
        coeff_b_a1_n = coeff_a_a1 - coeff_b_a1*c
        coeff_b_b1_n = coeff_a_b1 - coeff_b_b1*c
        coeff_a_a1 = coeff_a_a1_n
        coeff_a_b1 = coeff_a_b1_n
        coeff_b_a1 = coeff_b_a1_n
        coeff_b_b1 = coeff_b_b1_n
        a = b
        b = d

p = 0x1630754518592437521810394623170439071787346163136715732951116994613647026908158243257902189

import random

if __name__ == "__main__":
    k = 15
    
    print("k = %d" % k)
    print()
    
    points_x = Vec([Mod(random.randint(0, p - 1), p) for i in range(k)])
    points_y = Vec([Mod(random.randint(0, p - 1), p) for i in range(k)])
    
    print("INDIVIDUAL KEYS X")
    print(points_x)
    print()
    
    print("INDIVIDUAL KEYS Y")
    print(points_y)
    print()
    
    # run polynomial fitting with degree k - 1
    lhs = vander(points_x, k)
    rhs = points_y
    solution = (dotinv(lhs)*rhs).getcol(0)
    
    def fit_func(x, coeffs):
        rev = coeffs.d[::-1]
        t = 1
        out = 0
        for i in range(len(rev)):
            out += t*rev[i]
            t *= x
        return out
    
    # test fitting
    for i in range(k):
        x = points_x.d[i]
        y = points_y.d[i]
        assert(fit_func(x, solution) == y)
    
    import hashlib
    
    print("COMPOUND KEY")
    print(solution)
    print()
    
    print("COMPOUND KEY (HASH)")
    print(hashlib.sha256(str(solution).encode()).hexdigest())
