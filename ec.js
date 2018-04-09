elliptic = require("elliptic")
ec = elliptic.ec("secp256k1")

key = ec.keyFromPrivate("4545e45bae6aed7e1661208d5fb57473f4902b0cfe365de7f72eab60db999cda")
key.getPublic()

key.sign(10000)