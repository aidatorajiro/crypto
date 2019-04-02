import hashlib

def I2OSP(a, n):
    

def bytexor(a, b):
    return (int.from_bytes(a, 'little') ^ int.from_bytes(b, 'little')).to_bytes(max(len(a), len(b)), 'little')

def MGF1(seed, masklen, hashfunc, hashlen):
    out = b""
    for i in range(0, masklen // hashlen + 1):
        counter = i.to_bytes(4, "big")
        out += hashfunc(seed + counter)
    return out[0:masklen]

def EMSA_PSS_VERIFY(message, encoded, hashfunc, hashlen, saltlen):
    mesHash = hashfunc(message)
    print(len(mesHash))
    print(mesHash)
    maskedDB = encoded[:- hashlen - 1]
    print(len(maskedDB))
    print(maskedDB)
    encHash = encoded[- hashlen - 1:-1]
    print(len(encHash))
    print(encHash)
    mask = MGF1(encHash, len(encoded) - hashlen - 1, hashfunc, hashlen)
    print(len(mask))
    print(mask)
    DB = bytexor(maskedDB, mask)
    print(len(DB))
    print(DB)
    salt = DB[-saltlen:]
    print(len(salt))
    print(salt)
    calcHash = hashfunc(b"\x00\x00\x00\x00\x00\x00\x00\x00" + mesHash + salt)
    print(len(calcHash))
    print(calcHash)
    return encHash == calcHash

msg = bytes.fromhex("52b410815b9aa0afee00e873e2803ca5aa54e6dfc1aace3a5e2357bc04fe4461")

sig = 0x5729efd900e27265e48116452ec62292f38c66deeb961c233a91b7e0dde7c61ceee22b5ec2b9bba997e173cd0349f3a98a3461515c36af1df14b9e863e8b51716dcc197798a15b1e3dd47f2b712603f803cd2d1c6b8399e3396932fac5b45bdf309794d8b7dbf7e0536dfb625f029238a2dea742e057add005a1affd985ac32b7ea2262b3c65f64ff9fe8ef40803fa130c6ed853cdad842354feee8a845877533027351b8d9b970b78e18fd1c5096b5abe6509609a84ec410cd95fb164e56e83450dedad636050e8700ae0116eea730027145a6632be18ce778847aeb1c038ad4cdd621aa50dee4a86e1f891178a8e7801d0035faa98bc4eb55a1914148a222b

mod = 0x00ce7f8566037c84c305294dc3ff27d9f12a1cb9c942a82ba2c42a14d632317eebe99fed11894af5d1ce079d1e092d52356cd5ba74aa36e7f99885c6a312deb9cbe880ca23204b9a11bde1941ab3b00357a7796fb6921b3b19e2a4696807f33739dcd0416222697eaa0e455cf9bfed10bf95b19514f625f6f9a5e208cb30974da2cf61d773e563346b0cce51fd7d056a3ae8cd3a6783444a3abc02e6a36df3faa1c8457a883b04c63c7244766f385091a24ec752761f06a2a09171683c7623161b09e9c459980c29354556e759f57d79ae6fd39c115ad4b4eb18c07f8328e93b3ddf9be8a79c2e2425209bf72693ded68389548d1273c2e524fe9d057b5aac0e0b

enc = (pow(sig, 65537, mod)).to_bytes(256, "big")

hashfunc = lambda x: hashlib.sha256(x).digest()