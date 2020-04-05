# Statistics (and a little cryptography) over a finite field
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
    if type(a) == Mat and type(b) == Mat and a.m == b.n:
        l = []
        for i in range(a.n):
            for j in range(b.m):
                l.append(a.getrow(i)*b.getcol(j))
        return Mat(l, a.n, b.m)
    raise Exception("invalid argument")

# destructive function to perform a gaussian reduction
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
                mat.add_row_vec(j, coeff*mat.getrow(i))

def reduction_scale(mats):
    for i in range(mats[0].n):
        scale = 1/mats[0].pos(i, i)
        for mat in mats:
            mat.mul_row_with(i, scale)

class Mat(object):
    def __init__(self, d, n, m):
        assert len(d) == n*m
        self.d = d
        self.n = n
        self.m = m
    def getrow(self, i):
        assert i < self.n
        return tovec(self.d[i*self.m:(i + 1)*self.m])
    def getcol(self, i):
        assert i < self.m
        return tovec([self.d[t] for t in range(i, self.n*self.m, self.m)])
    def pos(self, x, y):
        return self.d[x*self.m + y]
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
            return Vec(list(map(lambda x: x*other, self.d)))
    def __rmul__(self, other):
        # self is right, other is left
        if type(other) == list or type(other) == Vec:
            other = tovec(other)
            return mat_dot(other, self)
        else:
            return Vec(list(map(lambda x: other*x, self.d)))
    def __truediv__(self, other):
        if type(other) == list or type(other) == Vec:
            pass
        else:
            return Vec(list(map(lambda x: x/other, self.d)))
    def __rtruediv__(self, other):
        if type(other) == list or type(other) == Vec:
            pass
        else:
            return Vec(list(map(lambda x: other/x, self.d)))
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


# tests
#from kusa3 import *

test_mat_1 = Mat([1,2,3,4,5,6], 2, 3)
test_mat_2 = Mat([7,8,9,10,11,12], 3, 2)

assert test_mat_1.getrow(0) == [1,2,3]
assert test_mat_1.getrow(1) == [4,5,6]
assert test_mat_1.getcol(1) == [2,5]

assert test_mat_1*test_mat_2 == Mat([58, 64, 139, 154], 2, 2)

test_mat_3 = Mat([1,2,3,4,5,6], 2, 3)
test_mat_3.add_row_vec(1, Vec([1,1,1]))
assert test_mat_3 == Mat([1,2,3,5,6,7], 2, 3)
assert -Vec([1,1,1]) == Vec([-1,-1,-1])
assert -Mat([1,2,3,4,5,6], 2, 3) == Mat([-1,-2,-3,-4,-5,-6], 2, 3)
assert Vec([1,1,1])/2 == Vec([1/2,1/2,1/2])
assert Vec([1,1,1])*2 == Vec([2,2,2])
assert 2/Vec([1,1,1]) == Vec([2,2,2])
assert 2*Vec([1,1,1]) == Vec([2,2,2])

test_mat_4 = Mat([5,3,6,2,6,7,1,3,6], 3, 3)
test_mat_4_orig = Mat(test_mat_4.d.copy(), 3, 3)
test_mat_5 = mat_identity(3)
reduction([test_mat_4, test_mat_5], "up")
reduction([test_mat_4, test_mat_5], "down")
reduction_scale([test_mat_4, test_mat_5])
print(test_mat_4_orig*test_mat_5)

p = 0x1630754518592437521810394623170439071787346163136715732951116994613647026908158243257902189


"""
import numpy as np
import random
from numpy.lib.twodim_base import vander

# based on https://integratedmlai.com/matrixinverse/
def invert_matrix(A, tol=None):
 
    # Section 2: Make copies of A & I, AM & IM, to use for row ops
    n = len(A)
    AM = A.copy()
    IM = np.identity(n, dtype=object)
 
    # Section 3: Perform row operations
    indices = list(range(n)) # to allow flexible row referencing ***
    for fd in range(n): # fd stands for focus diagonal
        fdScaler = 1 / AM[fd][fd]
        # FIRST: scale fd row with fd inverse. 
        for j in range(n): # Use j to indicate column looping.
            AM[fd][j] *= fdScaler
            IM[fd][j] *= fdScaler
        # SECOND: operate on all rows except fd row as follows:
        for i in indices[0:fd] + indices[fd+1:]: 
            # *** skip row with fd in it.
            crScaler = AM[i][fd] # cr stands for "current row".
            for j in range(n): 
                # cr - crScaler * fdRow, but one element at a time.
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                IM[i][j] = IM[i][j] - crScaler * IM[fd][j]
    
    return IM

k = 15

points_x = np.array([Mod(random.randint(0, p - 1), p) for i in range(k)])
points_y = np.array([Mod(random.randint(0, p - 1), p) for i in range(k)])

#points_x = np.array([random.random() for i in range(k)])
#points_y = np.array([random.random() for i in range(k)])

print("INDIVIDUAL KEYS X")
print(points_x)
print("INDIVIDUAL KEYS Y")
print(points_y)

# run polynomial fitting with degree k - 1
lhs = vander(points_x, k)
rhs = points_y
solution = invert_matrix(lhs).dot(rhs)

def fit_func(x, coeffs):
    rev = coeffs[::-1]
    t = 1
    out = 0
    for i in range(len(rev)):
        out += t*rev[i]
        t *= x
    return out

# test fitting
for i in range(k):
    x = points_x[i]
    y = points_y[i]
    assert(fit_func(x, solution) == y)

import hashlib

print("COMPOUND KEY")
print(solution)

print("COMPOUND KEY (HASH)")
print(hashlib.sha256(str(solution).encode()).hexdigest())
"""