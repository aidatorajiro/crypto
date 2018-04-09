contract Keisan {
    uint constant p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f;
    uint constant a = 0x0;
    uint constant b = 0x7;
    uint constant gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798;
    uint constant gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8;
    
    function powmod(uint b, uint e, uint m) private constant returns (uint r) {
        r = 1;
        uint bit = 2 ** 255;
        assembly {
            loop:
                jumpi(end, iszero(bit))
                r := mulmod(mulmod(r, r, m), exp(b, iszero(iszero(and(e, bit)))), m)
                r := mulmod(mulmod(r, r, m), exp(b, iszero(iszero(and(e, div(bit, 2))))), m)
                r := mulmod(mulmod(r, r, m), exp(b, iszero(iszero(and(e, div(bit, 4))))), m)
                r := mulmod(mulmod(r, r, m), exp(b, iszero(iszero(and(e, div(bit, 8))))), m)
                bit := div(bit, 16)
                jump(loop)
            end:
        }
    }
    
    function add(uint px, uint py, bool is_p_origin, uint qx, uint qy, bool is_q_origin) pure returns (uint, uint) {
        if (is_p_origin) {
            return (qx, qy);
        } else if () {}
    }
}