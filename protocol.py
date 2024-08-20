from hash_helpers import digest
from math_helpers import rand_less_than

class Signer:
    def __init__(self, parameters):
        self.parameters = parameters
        self.keypair = choose_keypair(self.parameters)

    def start(self, info):
        self.z = digest(info, self.parameters)

    def one(self):
        self.u, self.s, self.d = [rand_less_than(self.parameters['q'], self.parameters['N']) for _ in range(3)]
        self.a = pow(self.parameters['g'], self.u, self.parameters['p'])
        self.b = (pow(self.parameters['g'], self.s, self.parameters['p']) *
                  pow(self.z, self.d, self.parameters['p'])) % self.parameters['p']
        return self.a, self.b

    def three(self, e):
        self.c = (e - self.d) % self.parameters['q']
        self.r = (self.u - (self.c * self.keypair['x'])) % self.parameters['q']
        return self.r, self.c, self.s, self.d

class User:
    def __init__(self, parameters, pubkey):
        self.parameters = parameters
        self.y = pubkey

    def start(self, info, msg):
        self.t1, self.t2, self.t3, self.t4 = [rand_less_than(self.parameters['q'], self.parameters['N']) for _ in range(4)]
        self.z = digest(info, self.parameters)
        self.msg = msg

    def two(self, a, b):
        alpha = (a * pow(self.parameters['g'], self.t1, self.parameters['p']) *
                 pow(self.y, self.t2, self.parameters['p'])) % self.parameters['p']
        beta = (b * pow(self.parameters['g'], self.t3, self.parameters['p']) *
                pow(self.z, self.t4, self.parameters['p'])) % self.parameters['p']
        e_bytes = bytearray()
        for v in (alpha, beta, self.z):
            e_bytes.extend(int_to_bytes(v))
        e_bytes.extend(self.msg)
        epsilon = int.from_bytes(full_domain_hash(e_bytes, self.parameters['N']), 'little')
        return (epsilon - self.t2 - self.t4) % self.parameters['q']

    def four(self, r, c, s, d):
        rho = (r + self.t1) % self.parameters['q']
        omega = (c + self.t2) % self.parameters['q']
        delta = (s + self.t3) % self.parameters['q']
        sigma = (d + self.t4) % self.parameters['q']
        return rho, omega, delta, sigma
