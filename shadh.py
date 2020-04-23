import hashlib

O = 'Origin'

def add3(P,Q,R):
    def dig2(P, Q):
        obj = hashlib.sha256()
        obj.update(P.to_bytes(32, "little") + Q.to_bytes(32, "little"))
        return int.from_bytes(obj.digest(), 'little')
    
    l = [P,Q,R]
    
    o_cnt = l.count(O)
    
    if o_cnt == 0:
        ret = dig2(P,Q) + dig2(Q,R) + dig2(R,P) + dig2(Q,P) + dig2(R,Q) + dig2(P,R)
    if o_cnt == 1:
        [A, B] = filter(lambda x: x != O, l)
        ret = dig2(A,B) + dig2(B,A)
    if o_cnt == 2:
        [A] = filter(lambda x: x != O, l)
        ret = A
    if o_cnt == 3:
        return O
    
    return ret % (2**256)

def add(P, Q):
    

"""
def add(P, Q):
    if P == O:
        return Q
    if Q == O:
        return P
    
    obj1 = hashlib.sha256()
    obj1.update(P.to_bytes(32, "little") + Q.to_bytes(32, "little"))
    dig1 = int.from_bytes(obj1.digest(), 'little')
    
    obj2 = hashlib.sha256()
    obj2.update(Q.to_bytes(32, "little") + P.to_bytes(32, "little"))
    dig2 = int.from_bytes(obj2.digest(), 'little')
    
    return (dig1 + dig2) % (2**256)
"""

def mul(P, n):
  bs = format(n, 'b')[::-1]
  tmp = P
  result = O
  for i in bs:
    if i == "1":
      result = add(result, tmp)
    tmp = add(tmp, tmp)
  return result
