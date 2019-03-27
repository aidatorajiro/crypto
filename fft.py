import math
import random
from matplotlib import pyplot as plt

def ft(vec, cycle, mod=None):
    N = len(vec)
    out = []
    for i in range(N):
        s = 0
        for j in range(N):
            s += vec[j]*cycle[(i*j)%N]
        if mod != None:
            s %= mod
        out.append(s)
    return out

def fft(vec, cycle, mod=None):
    if len(vec) == 4:
        return ft(vec, cycle, mod)
    else:
        N = len(vec)
        N2 = N//2
        cycle2 = [cycle[i] for i in range(0, N, 2)]

        even = fft([vec[i] for i in range(0, N, 2)], cycle2)
        odd = fft([vec[i] for i in range(1, N, 2)], cycle2)

        ret = []
        for i in range(0, N2):
            d = even[i] + odd[i]*cycle[i]

            if mod != None:
                d %= mod

            ret.append(d)
        for i in range(0, N2):
            d = even[i] + odd[i]*cycle[(i + N2)%N] # ROTATE BY N2 THEN ADD

            if mod != None:
                d %= mod

            ret.append(d)
        return ret

# cycle for a complex Fourier transform
def complex_cycle(n):
    ret = []
    for i in range(n):
        theta = -2*math.pi*i/n
        ret.append(complex(math.cos(theta), (math.sin(theta))))
    return ret

# calculate inverse cycle
def cycle_inverse(cycle):
    N = len(cycle)
    return [cycle[0]] + cycle[::-1][:N - 1]

def example_ft():
    N = 256
    sourcewave = []
    for i in range(N):
        theta = 2*math.pi*i/N
        sourcewave.append(math.cos(50*theta) + math.sin(30*theta) + 0.6*math.sin(20*theta))

    dat = ft(sourcewave, complex_cycle(N))

    plt.plot(list(map(lambda x: x.real/N*2, dat)))
    plt.plot(list(map(lambda x: x.imag/N*2, dat)))
    plt.show()

def example_fft():
    N = 32768
    sourcewave = []
    for i in range(N):
        theta = 2*math.pi*i/N
        sourcewave.append(math.cos(3822*theta) + math.cos(1222*theta) + 6.9*math.cos(12000*theta))

    dat = fft(sourcewave, complex_cycle(N))

    plt.plot(list(map(lambda x: x.real/N*2, dat)))
    plt.plot(list(map(lambda x: x.imag/N*2, dat)))
    plt.show()

def example_nfft():
    N = 256
    p = N + 1

    val = 1
    cycle = []
    for i in range(N):
        cycle.append(val)
        val = val*13%p

    sourcewave = list(range(N))

    print("Cycle: %s" % cycle)
    print("Input Vector: %s" % sourcewave)
    print("Result(FT): %s" % ft(sourcewave, cycle, p))
    print("Result(FFT): %s" % fft(sourcewave, cycle, p))

def example_numeric_convolution():
    N = 256
    p = N + 1

    val = 1
    cycle = []
    for i in range(N):
        cycle.append(val)
        val = val*13%p

    vec1 = list(range(N))
    vec2 = list(range(N, 0, -1))

    conv = []
    for i in range(N):
        s = 0
        for j in range(i + 1):
            s += vec1[j]*vec2[i - j]
        s %= p
        conv.append(s)

    vec1f = fft(vec1, cycle, p)
    vec2f = fft(vec2, cycle, p)

    vec3f = []
    for i in range(N):
        vec3f.append(vec1f[i] * vec2f[i] % p)

    vec3 = fft(vec3f, cycle_inverse(cycle), p)

    print("Vec1: %s" % vec1)
    print("Vec2: %s" % vec2)
    print("F^-1(F(Vec1) . F(Vec2)): %s" % vec3)
    print("Vec1*Vec2: %s" % conv)

#example_ft()
#example_fft()
#example_nfft()
example_numeric_convolution()
