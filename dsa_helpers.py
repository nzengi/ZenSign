from math_helpers import rand_prime, rand_less_than, rand_int

def choose_q(N):
    return rand_prime(N)

def choose_p(L, N, q):
    k = L - N
    while True:
        p = (q * rand_int(k)) + 1
        if prime_test(p, L):
            return p

def choose_g(L, N, p, q):
    h = 2
    while True:
        g = pow(h, (p - 1) // q, p)
        if pow(g, q, p) == 1:
            return g
        h += 1

def choose_parameters(L, N):
    q = choose_q(N)
    p = choose_p(L, N, q)
    g = choose_g(L, N, p, q)
    return {'L': L, 'N': N, 'p': p, 'q': q, 'g': g}

def choose_keypair(parameters):
    x = rand_less_than(parameters['q'], parameters['N'])
    y = pow(parameters['g'], x, parameters['p'])
    return {'x': x, 'y': y, 'parameters': parameters}
