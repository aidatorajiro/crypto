var mnemonic = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon'

var crypto = require('crypto')
var EC = require('elliptic').ec
var ec = new EC('secp256k1')
var HDKey = require('hdkey')
var bip39 = require('bip39')
var bs58 = require('bs58')
var hd = HDKey.fromMasterSeed(bip39.mnemonicToSeed(mnemonic))

var derived = hd.derive("m/44'/0'/0'/0/0") // testnet: var derived = hd.derive("m/44'/1'/0'/0")
var privKey = derived.privateKey
var pubKey = ec.g.mul(privKey)
var compressedPubKey = Buffer.from(pubKey.encodeCompressed())

// pubKeyHash = ripemd160(sha256(compressedPubKey))
var pubKeyHash = crypto.Hash('ripemd160').update(crypto.Hash('sha256').update(compressedPubKey).digest()).digest()

assert(derived.publicKey.equals(compressedPubKey))
assert(derived.pubKeyHash.equals(pubKeyHash))

var pubKeyHashWithID = Buffer.concat([Buffer.from([0x00]), pubKeyHash]) // testnet: var pubKeyHashWithID = Buffer.concat([Buffer.from([0x6F]), pubKeyHash])
var checksum = crypto.Hash('sha256').update(crypto.Hash('sha256').update(pubKeyHashWithID).digest()).digest().slice(0, 4)
var addr = bs58.encode(Buffer.concat([pubKeyHashWithID, checksum]))

// extract private key from secret: bs58.decode("L3E3DNW5wtHfT3Gjkhx5X7JynPbFpTksBXYkftN1mmaYU3soLNXk").slice(1,33)