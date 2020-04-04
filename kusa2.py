# Statistics (and a little cryptography) over a finite field
# polynomial fitting
# use numpy

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

"""
class Mat(object):
    def __init__(self, d, n, m):
        self.d = d
        self.n = n
        self.m = m
    def reduction(self, v):
        
    def pos(self, x, y):
        return self.d[x*self.m + y]
    def __add__(self, other):
        return [self.d[i] + other.d[i] for i in range(self.n*self.m)]
    def __radd__(self, other):
        return [self.d[i] + other.d[i] for i in range(self.n*self.m)]
    def __mul__(self, other):
        # self is left, other is right
        
    def __rmul__(self, other):
        # self is right, other is left
"""

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

import numpy as np
import random
from numpy.lib.twodim_base import vander

# https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy very simple invert func
def transposeMatrix(m):
    return list(map(list,zip(*m)))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

k = 4

points_x = np.array([Mod(random.randint(0, p - 1), p) for i in range(k)])
points_y = np.array([Mod(random.randint(0, p - 1), p) for i in range(k)])

print("INDIVIDUAL KEYS X")
print(points_x)
print("INDIVIDUAL KEYS Y")
print(points_y)

#points_x = np.array([random.random() for i in range(k)])
#points_y = np.array([random.random() for i in range(k)])

# run polynomial fitting with degree k - 1
lhs = vander(points_x, k)
rhs = points_y
solution = np.array(getMatrixInverse(lhs.tolist())).dot(rhs)

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
print(hashlib.sha256(str(solution).encode()).hexdigest())