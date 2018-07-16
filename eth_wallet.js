var mnemonic = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon'

var EC = require('elliptic').ec
var ec = new EC('secp256k1')
var HDKey = require('hdkey')
var bip39 = require('bip39')
var ent = bip39.mnemonicToSeed(mnemonic)
var hd = HDKey.fromMasterSeed(ent)

var SHA3 = require('sha3')

var d = new SHA3.SHA3Hash(256)

var privKey = hd.derive("m/44'/60'/0'/0/0").privateKey
var pubKey = ec.g.mul(privKey)

d.update(Buffer.concat([pubKey.x.toBuffer(), pubKey.y.toBuffer()]))
var address = d.digest('hex').slice(24) // the account address

var Web3 = require('web3')

var web3 = new Web3(new Web3.providers.HttpProvider("http://mainnet.infura.io/"))

