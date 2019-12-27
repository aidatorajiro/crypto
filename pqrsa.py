# Very simple pqrsa implementation / key generation around 5min (1024-bit primes*1024, 1048576-bit encryption)

import random
import gmpy2

# pure python implementation
def is_prime(n):
    if n == 2: return True
    if n == 1 or n & 1 == 0: return False
    d = (n - 1) >> 1
    while d & 1 == 0:
        d >>= 1
    for k in range(100):
        a = random.randint(1, n - 1)
        t = d
        y = pow(a, t, n)
        while t != n - 1 and y != 1 and y != n - 1:
            y = (y * y) % n
            t <<= 1
        if y != n - 1 and t & 1 == 0:
            return False
    return True

kazu_1 = 1 # public key
kazu_2 = 1 # phi(public key) must be destroyed
count = 0

random.seed(114514) # master key

while count < 1024:
    kazu = random.randint(2**1022, 2**1023 - 1)
    prm = kazu*2 + 1
#   stat = random.getstate()
#   if is_prime(prm):
#       random.setstate(stat)
    if gmpy2.is_prime(prm):
        kazu_1 *= prm
        kazu_2 *= prm - 1
        count += 1
        print(count)
        print(prm)

e = 1145141

with open("./pubkey", "w") as f:
    f.write(hex(kazu_1))

with open("./key_enc", "w") as f:
    f.write(hex(e))

# extended euc
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

d = ext_euc(kazu_2, e)[7] % kazu_2

with open("./key_dec", "w") as f:
    f.write(hex(d))
