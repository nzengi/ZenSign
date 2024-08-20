from hash_helpers import int_to_bytes, full_domain_hash

def check(rho, omega, delta, sigma, z, msg, y, parameters):
    lhs = int_to_bytes((omega + sigma) % parameters['q'])
    rhs_one = (pow(parameters['g'], rho, parameters['p']) *
               pow(y, omega, parameters['p'])) % parameters['p']
    rhs_two = (pow(parameters['g'], delta, parameters['p']) *
               pow(z, sigma, parameters['p'])) % parameters['p']
    rhs_hash = full_domain_hash(int_to_bytes(rhs_one) + int_to_bytes(rhs_two) +
                                int_to_bytes(z) + msg, parameters['N'])
    rhs = int_to_bytes(int.from_bytes(rhs_hash, 'little') % parameters['q'])
    return rhs == lhs
