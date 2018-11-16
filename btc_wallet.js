const assert = require('assert');
const readlineSync = require('readline-sync');

var mnemonic = readlineSync.question("Mnemonic: ")
var derivation = readlineSync.question("Derivation Path (like m/44'/0'/0'/0/0): ")

let network = "mainnet"; // mainnet | testnet | regtest
let encodeType = "bech32"; // base64 | bech32
let purpose = "p2wpkh"; // p2pkh | p2wpkh-nested-in-p2sh | p2wpkh; if encodeType == bech32, MUST BE p2wpkh. if encodeType == base64, MUST BE either p2pkh or p2wpkh-nested-in-p2sh. p2pkh -> 20 byte key hash, p2wpkh-nested-in-p2sh -> 20 byte script hash (hash of 0014<20 byte key hash>), p2wpkh -> 20 byte key hash.

let crypto = require('crypto')
let EC = require('elliptic').ec
let ec = new EC('secp256k1')
let HDKey = require('hdkey')
let bip39 = require('bip39')
let bs58 = require('bs58')
let segwit_addr = require('./segwit_addr')
let hd = HDKey.fromMasterSeed(bip39.mnemonicToSeed(mnemonic))

let derived = hd.derive(derivation) // testnet: var derived = hd.derive("m/44'/1'/0'/0/0")
let privKey = derived.privateKey
let pubKey = ec.g.mul(privKey)
let compressedPubKey = Buffer.from(pubKey.encodeCompressed())

let sha256 = (x) => crypto.Hash('sha256').update(x).digest()
let hash160 = (x) => (crypto.Hash('ripemd160').update(crypto.Hash('sha256').update(x).digest()).digest())

// pubKeyHash = ripemd160(sha256(compressedPubKey))
let pubKeyHash = hash160(compressedPubKey)

assert(derived.publicKey.equals(compressedPubKey))
assert(derived.pubKeyHash.equals(pubKeyHash))
console.log("Priv key: " + privKey.toString("hex"))
console.log("Pub key: (x: " + pubKey.x.toString("hex") + ", y: " + pubKey.y.toString("hex") + ")")
console.log("Pub key hash: " + pubKeyHash.toString("hex"))

/*
function bech32_polymod (values) {
    let GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    let chk = 1
    let b
    for (let v of values) {
        b = (chk >> 25)
        chk = (chk & 0x1ffffff) << 5 ^ v
        for (let i of [0, 1, 2, 3, 4]) {
            chk ^= ((b >> i) & 1) ? GEN[i] : 0
        }
    }
    return chk
}

function bech32_hrp_expand (s) {
    return [].concat(s.map((x) => (x >> 5)), [0], s.map((x) => (x & 31)))
}

function bech32_create_checksum(hrp, data) {
    values = [].concat(bech32_hrp_expand(hrp) + data)
    polymod = bech32_polymod([].concat(values, [0,0,0,0,0,0])) ^ 1
    return [0, 1, 2, 3, 4, 5].map((i) => ((polymod >> 5 * (5 - i)) & 31))
}
*/

let checksum
let addr
let encodeContent
let hrp

if (encodeType === "base64") {
    let script
    let scriptHash

    // calculate script hash for p2sh
    if (purpose === "p2wpkh-nested-in-p2sh") {
        script = Buffer.concat([Buffer.from([0x00, 0x14]), pubKeyHash])
        scriptHash = hash160(script)
    }

    if (network === "mainnet") {
        if (purpose === "p2pkh") {
            encodeContent = Buffer.concat([Buffer.from([0x00]), pubKeyHash])
        }
        if (purpose === "p2wpkh-nested-in-p2sh") {
            encodeContent = Buffer.concat([Buffer.from([0x05]), scriptHash]) // Will create P2WPKH nested in P2SH address.
        }
    }

    if (network === "testnet" || network === "regtest") {
        if (purpose === "p2pkh") {
            encodeContent = Buffer.concat([Buffer.from([0x6F]), pubKeyHash])
        }
        if (purpose === "p2wpkh-nested-in-p2sh") {
            encodeContent = Buffer.concat([Buffer.from([0xC4]), scriptHash]) // Will create P2WPKH nested in P2SH address.
        }
    }

    checksum = crypto.Hash('sha256').update(crypto.Hash('sha256').update(encodeContent).digest()).digest().slice(0, 4)
    addr = bs58.encode(Buffer.concat([encodeContent, checksum]))
}

if (encodeType === "bech32") {
    if (network === "mainnet") {
        hrp = "bc"
    }

    if (network === "testnet") {
        hrp = "tb"
    }

    if (network === "regtest") {
        hrp = "bcrt"
    }


    if (purpose === "p2wpkh") {
        encodeContent = pubKeyHash
    } else {
        throw new Error("p2wpkh is only supported")
    }

    addr = segwit_addr.encode(hrp, 0, encodeContent)
}

console.log("Address: " + addr)

// extract private key from secret: bs58.decode("L3E3DNW5wtHfT3Gjkhx5X7JynPbFpTksBXYkftN1mmaYU3soLNXk").slice(1,33)

// console.log(Buffer.from(bech32Decode("tb1qjplwffe53emuuus7uhrgzfkum5h45r5zsye38x").databytes))

