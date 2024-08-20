import os
import hashlib

def rand_int(nbits):
    if nbits % 8 != 0:
        raise ValueError("nbits must be divisible by 8.")
    return int.from_bytes(os.urandom(nbits // 8), byteorder='little')

def rand_less_than(upper_bound, nbits):
    while True:
        r = rand_int(nbits)
        if r < upper_bound:
            return r

def miller_rabin_test(p, nbits, k=5):
    r, d = 0, p - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = rand_less_than(p - 2, nbits) + 1
        x = pow(a, d, p)
        if x == 1 or x == p - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, p)
            if x == p - 1:
                break
        else:
            return False
    return True

def prime_test(p, nbits):
    return miller_rabin_test(p, nbits)

def rand_prime(nbits):
    while True:
        p = rand_int(nbits)
        if prime_test(p, nbits):
            return p
