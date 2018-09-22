/*====================
    Misc Functions
====================*/

/* Create elliptic a curve point from a x coordinate */
createPointFromX(E, x) = local(x = Mod(x, E.p)); [x, sqrt(x^3 + E[2]*x^2 + E[4]*x + E[5])]

/* Restore signer's public key from a signature */
restorePointFromSignature(E, G, N, r, s, m) = ellmul(E, ellsub(E, ellmul(E, createPointFromX(E, r), s), ellmul(E, G, m)), lift(Mod(r, N)^-1))

/* Hash x by algorithm a; zeropad to length l; requires Python3 */
hash(a, x, l) = extern("python3 -c \"import hashlib;print(int.from_bytes(hashlib.new('"a"', ("x").to_bytes("l", 'big')).digest(), 'big'))\"")

sha256(x, l) = hash("sha256", x, l)

/*=======================================
       X25519 Params And Functions
            BASED ON RFC 7748
=======================================*/

/* Curve for X25519 */
E25519 = ellinit(Mod([0, 486662, 0, 1, 0], 2^255 - 19));

/* Base point for X25519 */
G25519 = createPointFromX(E25519, 9)

/* switch endianness */
endian (x) = {
  local(r = 0);
  for (i = 0, 31, r += (bitand(x >> (i*8), 0xFF) << ((31-i)*8)));
  return(r);
}

/* decode a scalar */
decodeS (x) = {
  x = bitand(x, 2^256 - 1 - (7 << 248));
  x = bitand(x, 2^256 - 1 - 128);
  x = bitor(x, 64);
  return(endian(x));
}

/* decode a U coordinate to an E25519 point */
decodeU (x) = {
  x = bitand(x, 2^256 - 1 - 128);
  return(createPointFromX(E25519, endian(x)));
}

/* encode an E25519 point to a U coordinate */
encodeP (x) = endian(lift(x[1]))

/* multiplication test */
{
  local(k, P);
  k = decodeS(0xa546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4);
  P = decodeU(0xe6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c);
  encodeP(ellmul(E25519, P, k)) == 0xc3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552
}

/* ECDH test */
{
  local(Apriv, Apub, Bpriv, Bpub);
  Apriv = 0x77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a;
  Apub = ellmul(E25519, G25519, Apriv);
  Bpriv = 0x5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb;
  Bpub = ellmul(E25519, G25519, Bpriv);
  Asecret = ellmul(E25519, Bpub, Apriv);
  Bsecret = ellmul(E25519, Apub, Bpriv);
  Asecret == Bsecret
}

/*========================================
      SECP256R1 Params And Functions
========================================*/

/* Curve for SECP256R1 */
E256R1 = ellinit(Mod([0, 0, 0, -3, 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B], 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF));

/* Base point for SECP256R1 */
G256R1 = createPointFromX(E256R1, 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296)

/* Order for SECP256R1 */
N256R1 = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

/*========================================
                SSL TEST
========================================*/
server_pub = 0xc5f1603edee701bda2562cd7b8928ed44bd6d9f24f6e256996e01e293e9f0f45



/*
r = 0xbf9ce55d284c9f979d02472d2232139db6e1900dd3a01a66ffcc9b8ffd472760
s = 0x95b05992f43cd7bb69737cf563fdb49547f93ce7b24f9339aecbf2994b307d14
m = 0x9cbe7242dd8d58f91a51cfd1ccd130362bac0ec6618bcc64ae93b053c7c5309f

restorePointFromSignature(E256R1, G256R1, N256R1, r, s, m)

ellsub(E256R1, ellmul(E256R1, createPointFromX(E256R1, r), s), ellmul(E256R1, G256R1, m))
*/
