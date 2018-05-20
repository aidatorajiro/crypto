contract EC {
    uint constant p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f;
    uint constant a = 0x0;
    uint constant b = 0x7;
    uint constant gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798;
    uint constant gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8;
    
    function inv_mod_p(uint a) pure internal returns (uint) {
        if (a > p) {
            a = a % p;
        }
        int t1;
        int t2 = 1;
        uint r1 = p;
        uint r2 = a;
        uint q;
        while (r2 != 0) {
            q = r1 / r2;
            (t1, t2, r1, r2) = (t2, t1 - int(q) * t2, r2, r1 - q * r2);
        }
        if (t1 < 0) {
            return (p - uint(-t1));
        }
        return uint(t1);
    }
    
    function add(bool is_p_origin, uint px, uint py, bool is_q_origin, uint qx, uint qy) pure internal returns (bool o, uint x, uint y) {
        if (is_p_origin) {
            (o, x, y) = (is_q_origin, qx, qy);
        } else if (is_q_origin) {
            (o, x, y) = (is_p_origin, px, py);
        } else if (px == qx && py == p - qy) {
            (o, x, y) = (true, 0, 0);
        } else {
            uint dydx;
            if (px == qx && py == qy) {
                dydx = mulmod(px, px, p);
                dydx = mulmod(addmod(mulmod(3, dydx, p), a, p), inv_mod_p(mulmod(2, py, p)), p);
            } else {
                dydx = mulmod(addmod(qy, p - py, p), inv_mod_p(addmod(qx, p - px, p)), p);
            }
            o = false;
            x = addmod(addmod(mulmod(dydx, dydx, p), p - px, p), p - qx, p);
            y = addmod(mulmod(dydx, addmod(px, p - x, p), p), p - py, p);
        }
    }
    
    function mul(bool po, uint px, uint py, uint n) pure internal returns (bool o, uint x, uint y) {
        o = true;
        while(n != 0) {
            if (n & 1 != 0) {
                (o, x, y) = add(o, x, y, po, px, py);
            }
            (po, px, py) = add(po, px, py, po, px, py);
            n = n / 2;
        }
    }
}