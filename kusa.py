# Staitstics over finite field

p = 1472496406139038080061747225435918408612363218516349492634219
sqrt_exponent = (p + 1)//4

data = [1,2,3,4,5,6,7,8,9,10,11,2,3,4,4,1,5,7,9,3,4,6,8,1,111,2,331,3,56,1]

def ext_euc(a1, b1):
    a = a1
    b = b1
    c = 0
    d = 0
    
    coeff_a_a1 = 1
    coeff_a_b1 = 0
    coeff_b_a1 = 0
    coeff_b_b1 = 1
    
    while True:
        c = a // b
        d = a % b
        if d == 0:
            return [coeff_b_a1, coeff_b_b1]
        coeff_a_a1_n = coeff_b_a1
        coeff_a_b1_n = coeff_b_b1
        coeff_b_a1_n = coeff_a_a1 - coeff_b_a1*c
        coeff_b_b1_n = coeff_a_b1 - coeff_b_b1*c
        coeff_a_a1 = coeff_a_a1_n
        coeff_a_b1 = coeff_a_b1_n
        coeff_b_a1 = coeff_b_a1_n
        coeff_b_b1 = coeff_b_b1_n
        a = b
        b = d

def mod_inv(x, p):
    return ext_euc(x, p)[0] % p

variance = 0
mean = 0
inv_len_data = mod_inv(len(data), p)

for i in data:
    mean += i
    mean = mean % p

mod_inv(len(data), p)

mean = (mean * inv_len_data) % p

print("mean: %d" % mean)

for i in data:
    variance += (i - mean)**2
    variance = variance % p

variance = (variance * inv_len_data) % p

print("variance: %d" % variance)

stdvar = pow(variance, sqrt_exponent, p)

if (stdvar**2)%p == variance:
    print("stdvar: %d" % stdvar)
else:
    print("stdvar: N/A")


