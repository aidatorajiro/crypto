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

decrypted = gmpy2.powmod(encrypted, key_dec, pubkey)

