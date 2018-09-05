createPointFromX(E, x) = [x, sqrt(x^3 + E[2]*x^2 + E[4]*x + E[5])]

p = 2^255 - 19

A = Mod(486662, p)
B = Mod(1, p)

a = (3 - A^2) / (3*B^2)
b = (2*A^3 - 9*a) / (27*B^3)

offset = A/(3*B)

E = ellinit(Mod([a, b], p))
