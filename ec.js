elliptic = require("elliptic")
ec = elliptic.ec("secp256k1")
SHA3 = require('sha3')

key = ec.keyFromPrivate("2")
key.getPublic()

d = new SHA3.SHA3Hash(256)
d.update(Buffer.from(key.pub.x.toString('hex') + key.pub.y.toString('hex'), 'hex'))
console.log(d.digest('hex').slice(24))

