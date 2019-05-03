"""
a, b - keys
x, y - session keys
sa, sb - shared keys
"""

import itertools

import bytes_func
import gmpy2


rs = gmpy2.random_state()


def _encrypt_params():
    g, p = None, None
    q = gmpy2.mpz_urandomb(rs, 256)
    q = gmpy2.next_prime(q)
    while True:
        t = gmpy2.mpz_urandomb(rs, 768)
        p = gmpy2.mul(q, t)
        p = gmpy2.add(p, 1)
        if gmpy2.is_prime(p):
            break

    for r in itertools.count(2):
        g = gmpy2.powmod(r, t, p)
        if g > 1:
            break

    return g, p, q


def _key_pair(g, p, q):
    key = gmpy2.mpz_random(rs, q)
    key_pub = gmpy2.powmod(g, key, p)
    return key, key_pub


def _gen_keys(g, p, q):
    a, a_pub = _key_pair(g, p, q)
    x, x_pub = _key_pair(g, p, q)
    return a, a_pub, x, x_pub


def _shared_key(a, x, x_pub, b_pub, y_pub, p):
    l2 = 2 ** 128
    x_mod = gmpy2.t_mod_2exp(x_pub, 128)
    d = gmpy2.add(l2, x_mod)
    da = gmpy2.mul(d, a)
    xda = gmpy2.add(x, da)

    y_mod = gmpy2.t_mod_2exp(y_pub, 128)
    e = gmpy2.add(l2, y_mod)

    sa = gmpy2.powmod(b_pub, e, p)
    sa = gmpy2.mul(sa, y_pub)
    sa = gmpy2.f_mod(sa, p)
    sa = gmpy2.powmod(sa, xda, p)
    return sa


def _send_to_socket(sock, *args):
    values = ' '.join([str(arg) for arg in args])
    sock.send(values.encode())


def _receive_from_socket(sock):
    values = sock.recv(4096)
    return [int(value) for value in values.decode().split()]


def start_handshake(sock):
    gpq = _encrypt_params()
    a, a_pub, x, x_pub = _gen_keys(*gpq)
    _send_to_socket(sock, a_pub, x_pub, *gpq)
    b_pub, y_pub = _receive_from_socket(sock)
    sa = _shared_key(a, x, x_pub, b_pub, y_pub, gpq[1])
    return bytes_func.from_int(int(sa))[:32]


def accept_handshake(sock):
    a_pub, x_pub, *gpq = _receive_from_socket(sock)
    b, b_pub, y, y_pub = _gen_keys(*gpq)
    _send_to_socket(sock, b_pub, y_pub)
    sb = _shared_key(b, y, y_pub, a_pub, x_pub, gpq[1])
    return bytes_func.from_int(int(sb))[:32]


def test_shared_key():
    g, p, q = _encrypt_params()
    a, a_pub, x, x_pub = _gen_keys(g, p, q)
    b, b_pub, y, y_pub = _gen_keys(g, p, q)

    sa = _shared_key(a, x, x_pub, b_pub, y_pub, p)
    sb = _shared_key(b, y, y_pub, a_pub, x_pub, p)

    assert sa == sb, f'\nsa: {sa}\nsb: {sb}'
    print(f'shared key: {sa}')


if __name__ == '__main__':
    test_shared_key()
