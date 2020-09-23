# general key Encryption

def calc_inv_ind(ind):
    n = [0]*len(ind)
    for i, j in enumerate(ind):
        n[j] = i
    return n

def calc_permutation(ind, bs):
    n = [0]*len(ind)
    for i, j in enumerate(ind):
        n[j] = bs[i]
    return n

class EncException(Exception):
    pass

class Encryption:
    def forward(self, bs):
        raise EncException("forward not implemented")
    def backward(self, bs):
        raise EncException("backward not implemented")

class Permutation(Encryption):
    def __init__(self, ind):
        assert set(ind) == set([i for i in range(len(ind))])
        self.ind = ind
    def forward(self, bs):
        return calc_permutation(self.ind, bs)
    def backward(self, bs):
        inv_ind = calc_inv_ind(self.ind)
        return calc_permutation(inv_ind, bs)

class Xor(Encryption):
    def __init__(self, const):
        self.const = const
    def forward(self, bs):
        n = []
        for c, b in zip(self.const, bs):
            n.append(c^b)
        return n
    def backward(self, bs):
        return self.forward(bs) # backward is same as forward

class Rot(Encryption):
    def __init__(self, rot):
        self.rot = rot
    def forward(self, bs):
        return [bs[(i - self.rot) % len(bs)] for i in range(len(bs))]
    def backward(self, bs):
        return [bs[(i + self.rot) % len(bs)] for i in range(len(bs))]







