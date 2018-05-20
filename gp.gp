p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
E = ellinit([0,0,0,0,7]*Mod(1,p), p);
g = [0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8]
h = [0x90c74af33f31d922a23931f358a0354b7bcd5c765cc1fceacc3b3d197e1076f1, 0xa1c1011c097a6b3ffb4757c5683861ee6bd989645f04cc968ff697b6cf3d0a49]

ex = (p - 1)/E.no

(elltatepairing(E, g, g, E.no)^ex)^9
elltatepairing(E, g, ellmul(E, g, 9), E.no)^ex


(p - 1)/E.no