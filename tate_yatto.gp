p = 1611845387

E1 = ellinit([0,0,0,0,3]*Mod(1, p))
P1 = [1, 2]

l1 = ellorder(E1, P1)

d = (p^2-1)/l1

h = ffgen(Mod(x^2 + 1, p))

E1 = ellinit([0,0,0,0,3], h)
E2 = ellinit([0,0,0,0,3], h)
P2 = [h+6, sqrt((h+6)^3+3)]

elltatepairing(E1, ellmul(E1, P1, 1000), ellmul(E2, P2, 100), l1)^d

elltatepairing(E1, ellmul(E1, P1, 100), ellmul(E2, P2, 1000), l1)^d