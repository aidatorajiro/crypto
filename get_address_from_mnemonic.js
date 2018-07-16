var mnemonic = 'abandon'

var EC = require('elliptic').ec
var curve = new EC('secp256k1').curve
var HDKey = require('hdkey')
var bip39 = require('bip39')
var ent = bip39.mnemonicToSeed(mnemonic)
var hd = HDKey.fromMasterSeed(ent)

var SHA3 = require('sha3')

var d = new SHA3.SHA3Hash(256)

var pubKey = curve.pointFromX(hd.derive("m/44'/60'/0'/0/0")._publicKey.slice(1))

d.update(Buffer.concat([pubKey.x.toBuffer(), pubKey.y.toBuffer()]))
d.digest('hex').slice(24)

