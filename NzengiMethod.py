from dsa_helpers import choose_parameters
from protocol import Signer, User
from check_signature import check

if __name__ == '__main__':
    L, N = 1024, 160
    info = b'info'
    msg = b'my msg'

    params = choose_parameters(L, N)
    signer = Signer(params)
    signer.start(info)

    user = User(params, signer.keypair['y'])
    user.start(info, msg)

    a, b = signer.one()
    e = user.two(a, b)
    r, c, s, d = signer.three(e)
    rho, omega, delta, sigma = user.four(r, c, s, d)

    assert (params['p'] - 1) % params['q'] == 0
    assert ((params['p'] - 1) % (params['q']**2)) != 0
    assert check(rho, omega, delta, sigma, user.z, msg, user.y, params)
