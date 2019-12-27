with open("./pubkey", "r") as f:
    pubkey = int(f.read(), 16)

with open("./key_enc", "r") as f:
    key_enc = int(f.read(), 16)

with open("./key_dec", "r") as f:
    key_dec = int(f.read(), 16)

import gmpy2

import math
import sys

encrypted = gmpy2.powmod(11711737117, key_enc, pubkey)

def calc_list(target, modulo, redix = 8):
    lst = [1]
    for i in range(2**redix):
        print(i)
        lst.append(gmpy2.t_mod(gmpy2.mul(lst[-1], target), modulo))
    return lst

def power(lst, exponent, modulo, redix = 8):
    result = 1
    while True:
        ind = exponent & (2**redix - 1)
        result = gmpy2.t_mod(gmpy2.mul(result, lst[ind]), modulo)
        exponent = exponent >> redix
        print(sys.getsizeof(exponent))
        if exponent == 0:
        	break
    return result

lst = calc_list(encrypted, pubkey, 8)

decrypted = power(lst, key_dec, pubkey, 8)

