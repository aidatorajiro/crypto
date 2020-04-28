# monadic(!) crypto fun library

import segwit_addr
from collections import namedtuple

class ParseException(Exception):
  pass

class GenerateException(Exception):
  pass

class SignException(Exception):
  pass

def getStr(st, byte_length):
  if len(st) < byte_length:
    raise ParseException("getStr failed")
  return (st[byte_length:], st[:byte_length])

def getStrReversed(st, byte_length):
  (st, data) = getStr(st, byte_length)
  return (st, data[::-1])

def putStr(st, data):
  return st + data

def putStrReversed(st, data):
  return st + data[::-1]

def getIntLE(st, byte_length):
  (st, data) = getStr(st, byte_length)
  num = int.from_bytes(data, 'little')
  return (st, num)

def putIntLE(st, byte_length, num):
  data = num.to_bytes(byte_length, 'little')
  return st + data

def getConst(st, data):
  if not st[:len(data)] == data:
    raise ParseException("getConst match failed")
  return (st[len(data):], data)

putConst = putStr

def getOr(st, *funcs):
  for f in funcs:
    try:
      (st, ret) = f(st)
      return (st, ret)
    except ParseException:
      pass
  raise ParseException("getOr all failed")

def getThen(st, *funcs):
  for f in funcs:
    (st, ret) = f(st)
  return (st, ret)

def putThen(st, *funcs):
  for f in funcs:
    st = f(st)
  return st

def getLoop(st, func, num):
  retlist = []
  for i in range(num):
    (st, ret) = func(st)
    retlist.append(ret)
  return (st, retlist)

def putMap(st, func, arglist):
  return putThen(st, *map(lambda x: c(func, x), arglist))

# make a function with no arguments other than st.
def c(func, *args):
  return (lambda st: func(st, *args))

def getVI(st):
  return getOr(st,
    c(getThen, c(getConst, b"\xff"), c(getIntLE, 8)),
    c(getThen, c(getConst, b"\xfe"), c(getIntLE, 4)),
    c(getThen, c(getConst, b"\xfd"), c(getIntLE, 2)),
    c(getIntLE, 1)
  )

def putVI(st, num):
  if num <= 0xfc:
    return putIntLE(st, 1, num)
  elif num <= 0xffff:
    return putIntLE(putStr(st, b"\xfd"), 2, num)
  elif num <= 0xffffffff:
    return putIntLE(putStr(st, b"\xfe"), 4, num)
  elif num <= 0xffffffffffffffff:
    return putIntLE(putStr(st, b"\xff"), 8, num)
  else:
    raise GenerateException("putVI int too big")

Txin = namedtuple("Txin", ("hash", "index", "script", "seqno"))

def getTxin(st):
  (st, hash) = getStrReversed(st, 32)
  (st, index) = getIntLE(st, 4)
  (st, vi) = getVI(st)
  (st, script) = getStr(st, vi)
  (st, seqno) = getIntLE(st, 4)
  return (st, Txin(hash, index, script, seqno))

def putTxin(st, txin):
  st = putStrReversed(st, txin.hash)
  st = putIntLE(st, 4, txin.index)
  st = putVI(st, len(txin.script))
  st = putStr(st, txin.script)
  st = putIntLE(st, 4, txin.seqno)
  return st

Txout = namedtuple("Txout", ("amount", "script"))

def getTxout(st):
  (st, amount) = getIntLE(st, 8)
  (st, vi) = getVI(st)
  (st, script) = getStr(st, vi)
  return (st, Txout(amount, script))

def putTxout(st, txout):
  st = putIntLE(st, 8, txout.amount)
  st = putVI(st, len(txout.script))
  st = putStr(st, txout.script)
  return st

JoinSplit = namedtuple("JoinSplit", (
  "vpub_old",
  "vpub_new",
  "anchor",
  "nullifiers",
  "commitments",
  "ephemeralKey",
  "randomSeed",
  "vmacs",
  "zkproof",
  "encCiphertexts"
))

def getJoinSplit(st, version):
  (st, vpub_old) = getIntLE(st, 8)
  (st, vpub_new) = getIntLE(st, 8)
  (st, anchor) = getStr(st, 32)
  (st, nullifiers) = getLoop(st, c(getStr, 32), 2)
  (st, commitments) = getLoop(st, c(getStr, 32), 2)
  (st, ephemeralKey) = getStr(st, 32)
  (st, randomSeed) = getStr(st, 32)
  (st, vmacs) = getLoop(st, c(getStr, 32), 2)
  if version == 2 or version == 3:
    (st, zkproof) = getStr(st, 296)
  else:
    (st, zkproof) = getStr(st, 192)
  (st, encCiphertexts) = getLoop(st, c(getStr, 601), 2)
  return JoinSplit(
    vpub_old,
    vpub_new,
    anchor,
    nullifiers,
    commitments,
    ephemeralKey,
    randomSeed,
    vmacs,
    zkproof,
    encCiphertexts
  )

ShieldedSpend = namedtuple("ShieldedSpend", (
  "cv",
  "anchor",
  "nullifier",
  "rk",
  "zkproof",
  "spendAuthSig",
))

def getShieldedSpend(st):
  (st, cv) = getStr(st, 32)
  (st, anchor) = getStr(st, 32)
  (st, nullifier) = getStr(st, 32)
  (st, rk) = getStr(st, 32)
  (st, zkproof) = getStr(st, 192)
  (st, spendAuthSig) = getStr(st, 64)
  return (st, ShieldedSpend(
    cv,
    anchor,
    nullifier,
    rk,
    zkproof,
    spendAuthSig
  ))

ShieldedOutput = namedtuple("ShieldedOutput", (
  "cv",
  "cmu",
  "ephemeralKey",
  "encCipherText",
  "outCipherText",
  "zkproof",
))

def getShieldedOutput(st):
  (st, cv) = getStr(st, 32)
  (st, cmu) = getStr(st, 32)
  (st, ephemeralKey) = getStr(st, 32)
  (st, encCipherText) = getStr(st, 580)
  (st, outCipherText) = getStr(st, 80)
  (st, zkproof) = getStr(st, 192)
  return (st, ShieldedOutput(
    cv,
    cmu,
    ephemeralKey,
    encCipherText,
    outCipherText,
    zkproof,
  ))

Transaction = namedtuple("Transaction", (
  "version", 
  "groupid", 
  "txins", 
  "txouts", 
  "locktime", 
  "expiry", 
  "valuebalance",
  "shieldedspends",
  "shieldedoutputs",
  "joinsplits", 
  "joinsplitpubkey", 
  "joinsplitsig",
  "bindingsig"
))

def getTransaction(st):
  (st, version) = getIntLE(st, 4)

  version = version & 0x7FFFFFFF

  groupid = None
  if version >= 3:
    (st, groupid) = getIntLE(st, 4)
  
  (st, numTxins) = getVI(st)
  (st, txins) = getLoop(st, getTxin, numTxins)

  (st, numTxouts) = getVI(st)
  (st, txouts) = getLoop(st, getTxout, numTxouts)

  (st, locktime) = getIntLE(st, 4)

  expiry = None
  if version >= 3:
    (st, expiry) = getIntLE(st, 4)
  
  valuebalance = None
  shieldedspends = None
  shieldedoutputs = None
  if version >= 4:
    (st, valuebalance) = getIntLE(st, 8) # TODO to signed value
    (st, numShieldedspends) = getVI(st)
    (st, shieldedspends) = getLoop(st, getShieldedSpend, numShieldedspends)
    (st, numShieldedoutputs) = getVI(st)
    (st, shieldedoutputs) = getLoop(st, getShieldedOutput, numShieldedoutputs)
  
  joinsplits = None
  joinsplitpubkey = None
  joinsplitsig = None
  if version >= 2:
    (st, numJoinSplits) = getVI(st)
    (st, joinsplits) = getLoop(st, c(getJoinSplit, version), numJoinSplits)
    if numJoinSplits > 0:
      (st, joinsplitpubkey) = getStr(st, 32)
      (st, joinsplitsig) = getStr(st, 64)
  
  bindingsig = None
  if version >= 4 and numShieldedspends + numShieldedoutputs > 0:
    (st, bindingsig) = getStr(st, 64)
  
  return (st, Transaction(
    version, 
    groupid, 
    txins, 
    txouts, 
    locktime, 
    expiry, 
    valuebalance,
    shieldedspends,
    shieldedoutputs,
    joinsplits, 
    joinsplitpubkey, 
    joinsplitsig,
    bindingsig
  ))

def putTransaction(st, transaction):
  st = putIntLE(st, 4, transaction.version)
  st = putVI(st, len(transaction.txins))
  st = putMap(st, putTxin, transaction.txins)
  st = putVI(st, len(transaction.txouts))
  st = putMap(st, putTxout, transaction.txouts)
  st = putIntLE(st, 4, transaction.locktime)
  return st

def putPushdata(st, data):
  l = len(data)
  if 1 <= l <= 75:
    prefix = putIntLE(b'', 1, l)
  elif 76 <= l <= 0xff:
    prefix = putIntLE(b'\x4c', 1, l)
  elif 0x100 <= l <= 0xffff:
    prefix = putIntLE(b'\x4d', 2, l)
  elif 0x10000 <= l <= 0xffffffff:
    prefix = putIntLE(b'\x4e', 4, l)
  else:
    raise ParseException("putPushdata : invalid data length")
  return st + prefix + data

def getPushdata(st):
  (st, first_byte) = getIntLE(st, 1)
  if first_byte == 0x4c:
    (st, length) = getIntLE(st, 1)
  elif first_byte == 0x4d:
    (st, length) = getIntLE(st, 2)
  elif first_byte == 0x4e:
    (st, length) = getIntLE(st, 4)
  elif 1 <= first_byte <= 75:
    (st, length) = (st, first_byte)
  else:
    raise ParseException("getPushdata : invalid first byte")
  (st, data) = getStr(st, length)
  return (st, data)

SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3
SIGHASH_ANYONECANPAY = 0x80

def sha256d(x):
  return sha256(sha256(x))

import hashlib

def sha256(text):
  return hashlib.sha256(text).digest()
