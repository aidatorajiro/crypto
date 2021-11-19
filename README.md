# my crypto works

My codes on crypto.

# contents

## Misc

- README.md - this file
- fft.py - Fast Fourier Transform (WIP)
- package.json - package.json for `.js` files
- nanndah.py - key exchange (WIP)
- shadh.py - key exchange (WIP)
- general.py - general encryption system

## Elliptic Curve

- EC.sol - ECDSA in JS.
- EC2.sol - Elliptic Curve compution in Solidity.
- EC_test.js - Elliptic Curve test file
- ec.js - Elliptic curve address generation
- gp.gp - PARI/GP elliptic curve pairing
- zcash.gp - PARI/GP zcash (WIP)
- mont_to_wiel.gp - montgomery curve to weierstrass curve

### Python Fullscratch Project

These python scripts are greatly helped by the stackoverflow post : <https://stackoverflow.com/questions/31074172/elliptic-curve-point-addition-over-a-finite-field-in-python>. And here: <https://crypto.stanford.edu/pbc/notes/ep/tate.html> <https://github.com/herumi/ango>

- fullscratch_pairing_weil.py - fullscratch weil pairing.
- fullscratch_pairing_tate.py - fullscratch tate pairing.
- fullscratch.py - fullscratch ECDSA in python.
- fullscratch_address.py - fullscratch ECDSA address generation in python.
- fullscratch_elgamal.py - fullscratch EC elgamal in python. (WIP?)
- fullscratch_mod_elgamal.py - fullscratch EC modified elgamal in python.
- fullscratch_pairing.py - fullscratch EC pairing in python. (WIP?)
- fullscratch_takusan.py - fullscratch ECDSA in python (infinite loop).
- fullscratch_zcash.py - fullscratch zcash in python (WIP)
- fullscratch_zcash_2.py - fullscratch zcash in python (WIP)
- fullscratch_zero_prf.py - fullscratch elliptic curve zero knowledge proof in python.
- projection.py - fullscratch EC addition / multiplication / pairing. Using projection to improve performance.

## Blockchain
- HomomorphicTransaction.sol - additive homomorphic transaction in solidity
- HomomorphicTransaction_test.js - additive homomorphic transaction in solidity
- NestedSign.sol - ECDSA verifier in Solidity. Signed message in signed Ethereum transaction!
- bech32.js - copy of bech32.js by Pieter Wuille
- btc_wallet.js - bitcoin wallet
- eth_wallet.js - Ethereum wallet
- eth_wallet_2.js - Ethereum wallet (WIP)
- segwit_addr.js - SegWit address
- zclib.py - ZCash transaction parse library
- zcrpc.py - ZCash RPC

## Statistics and Machine Learning over a Finite Field
- kusa.py - mean, variance, Standard deviation (if exists) in a finite field
- kusa2.py - polynomial fitting over a finite field, using numpy
- kusa3.py - polynomial fitting (without loss) over a finite field, pure python Oddly faster than kusa2.py.
- kusa3.test.py - tests of kusa3.py
- kusa4.py - polynomial fitting (with loss) over a finite field, pure python (WIP)
- kusa4.test.py - tests of kusa4.py

## Learning with Error
- lwe_sugoi.py - Learning with error cryptosystem in python (requires library mpmath).

## Post-Quantum RSA (multi prime RSA)
- pqrsa.py - key generation
- pqrsa_decr.py - decrypt
- pqrsa_decr_2.py - decrypt

## Monoalphabetic Substitution Cryptosystem
- mono_decr.py - Simple decryptor.
- mono_kaiseki.py - Count each characters
- mono_shuukei.py - Count consecutive characters.
- monosol - Graphical monoalphabetic substitution solver using Vue.js. <http://aidatorajiro.github.io/crypto/monosol>

### Decrypting Romaji Ciphertext
- KWDLC - You have to download this from <https://github.com/ku-nlp/KWDLC> in order to run `mono_kana*.py`.
- mono_kana_cipher.txt - Ciphertext input for `mono_kana*.py`. You have to create this file.
  `"\n"` (LF) can be used as a separator.
- mono_kana_setting.py - Setting for `mono_kana*.py`. You have to create this file.
  Set the contents to `cipher_char_whitelist = "<all chars that appear in ciphertext>"`.  
  `cipher_char_whitelist` must be 23 character length.
- mono_kana1.py - Count each characters from KWDLC
- mono_kana2.py - PCA Analysis of neighbor count (separated matrix)
- mono_kana3.py - PCA Analysis of neighbor count (concatenated matrix)
- mono_kana4.py - PCA Analysis of neighbor count (separated matrix, use different normalization)
- mono_kana5.py - PCA Analysis of neighbor count (separated matrix, mono_kana_setting.py not needed)

## TLS 1.3 (X25519, EMSA_PSS_VERIFY, etc.)
- ssl.gp - fullscratch TLS 1.3 related program (WIP?)
- ssl2.gp - fullscratch TLS 1.3 related program (WIP?)
- tls13.py - fullscratch TLS 1.3 related program (WIP?)
