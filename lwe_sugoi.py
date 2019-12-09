# from https://en.wikipedia.org/wiki/Learning_with_errors#Public-key_cryptosystem

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

def dot(x, y):
    return sum(map(lambda x: x[0]*x[1], zip(x, y)))

def add(x, y):
    return [x[i] + y[i] for i in range(len(x))]

def add_vectors(matrix):
    return reduce(add, matrix, [0] * len(matrix[0]))

### consts
def genconsts(n = 128):
    p = random.choice(list(filter(lambda x: x >= n*n, prime(2*n*n))))
    #eps = (3.45678910111213141516)
    #m = (1 + eps)*(n + 1)*math.log(p)
    m = 5*n
    alp = lambda n: 1/(math.sqrt(n)*math.log(n))
    x = lambda: random.normalvariate(0, alp(n)/math.sqrt(2*math.pi)) % 1.0

    ### priv key
    s = [random.randint(0, p - 1) for i in range(n)]

    ### public key
    a = [[random.randint(0, p - 1) for i in range(n)] for i in range(m)]
    e = [x() for i in range(m)]
    b = [dot(a[i], s) + e[i] for i in range(m)]

    return (m, a, b, p, s)

### encryption
def encryption(bit, m, a, b, p):
    S = list(filter(lambda x: random.random() < 0.5, range(m)))

    if bit == 0:
        enc_a = add_vectors([a[i] for i in S])
        enc_b = sum([b[i] for i in S])
    else:
        enc_a = add_vectors([a[i] for i in S])
        enc_b = (p // 2) + sum([b[i] for i in S])

    enc = (enc_a, enc_b)

    return enc

### decryption

def decryption(enc, s, p):
    if enc[1] - dot(enc[0], s) < p//2:
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

    print("bit: " + str(bit))
    print("sum of a: " + str(sum(enc[0])))
    print("b: " + str(enc[1]))

    if bit == dec:
        print("ok")
    else:
        print("error")
    
