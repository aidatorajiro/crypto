p = 811

E1 = ellinit([0,0,0,0,3]*Mod(1, p))
P1 = [1, 2]
l1 = ellorder(E1, P1)

for(i=1, 1000, if((p^i-1)%l1,,tgt=i;break))

h = ffgen(ffinit(p,tgt))

E1 = ellinit([0,0,0,0,3], h)
E2 = ellinit([0,0,0,0,3], h)
P2 = [h+10, sqrt((h+10)^3+3)]

d = (p^tgt - 1)/l1

elltatepairing(E1, ellmul(E1, P1, 1000), ellmul(E2, P2, 100), l1)^d
elltatepairing(E1, ellmul(E1, P1, 100), ellmul(E2, P2, 1000), l1)^d