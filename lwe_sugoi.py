# https://en.wikipedia.org/wiki/Learning_with_errors#Public-key_cryptosystem
# Oded Regev, “On lattices, learning with errors, random linear codes, and cryptography,” in Proceedings of the thirty-seventh annual ACM symposium on Theory of computing (Baltimore, MD, USA: ACM, 2005), 84–93

import math
import random
from functools import reduce

def prime(a):
    flags = [True] * (a + 1)
    for i in range(2, int(math.sqrt(a) + 0.1) + 1):
        if not flags[i]:
            continue
        for j in range(i*i, a + 1, i):
            flags[j] = False
    lst = []
    for i in range(2, a + 1):
        if flags[i]:
            lst.append(i)
    return lst

def dot(x, y, p):
    return sum(map(lambda x: x[0]*x[1], zip(x, y))) % p

def add(x, y, p):
    return [(x[i] + y[i]) % p for i in range(len(x))]

def add_vectors(matrix, p):
    return reduce(lambda x, y: add(x, y, p), matrix, [0] * len(matrix[0]))

### consts
def genconsts(n = 128):
    p = random.choice(list(filter(lambda x: x >= n*n, prime(2*n*n))))
    #eps = (3.45678910111213141516)
    #m = (1 + eps)*(n + 1)*math.log(p)
    m = 5*n
    alp = lambda n: 1/(math.sqrt(n)*math.log(n))
    x = lambda: int(random.normalvariate(0, 10000*alp(n)/math.sqrt(2*math.pi))) # TODO

    ### priv key
    s = [random.randint(0, p - 1) for i in range(n)]

    ### public key
    a = [[random.randint(0, p - 1) for i in range(n)] for i in range(m)]
    e = [x() for i in range(m)]
    b = [(dot(a[i], s, p) + e[i]) % p for i in range(m)]

    return (m, a, b, p, s)

### encryption
def encryption(bit, m, a, b, p):
    S = list(filter(lambda x: random.randint(0, 1) == 0, range(m)))

    if bit == 0:
        enc_a = add_vectors([a[i] for i in S], p)
        enc_b = sum([b[i] for i in S]) % p
    else:
        enc_a = add_vectors([a[i] for i in S], p)
        enc_b = ((p // 2) + sum([b[i] for i in S])) % p

    enc = (enc_a, enc_b)

    return enc

### decryption

def decryption(enc, s, p):
    value = (enc[1] - dot(enc[0], s, p)) % p
    distance_zero = min(value, p - value)
    distance_half = abs(value - p//2)
    if distance_zero < distance_half:
        dec = 0
    else:
        dec = 1
    
    return dec

### some test ...

(m, a, b, p, s) = genconsts()
samples = 100
for i in range(samples):
    bit = random.randint(0, 1)
    enc = encryption(bit, m, a, b, p)
    dec = decryption(enc, s, p)

    if bit == dec:
        print("ok")
    else:
        print("error")
