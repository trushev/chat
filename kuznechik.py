from functools import reduce

import bytes_func


_kpi = [
    252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77,
    233, 119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193,
    249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79,
    5, 132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31,
    235, 52, 44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204,
    181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135,
    21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177,
    50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87,
    223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3,
    224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74,
    167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65,
    173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59,
    7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217, 231, 137,
    225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133, 97,
    32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82,
    89, 166, 116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182
]

_reverse_kpi = [
    0xa5, 0x2d, 0x32, 0x8f, 0x0e, 0x30, 0x38, 0xc0, 0x54, 0xe6, 0x9e, 0x39, 0x55, 0x7e, 0x52, 0x91,
    0x64, 0x03, 0x57, 0x5a, 0x1c, 0x60, 0x07, 0x18, 0x21, 0x72, 0xa8, 0xd1, 0x29, 0xc6, 0xa4, 0x3f,
    0xe0, 0x27, 0x8d, 0x0c, 0x82, 0xea, 0xae, 0xb4, 0x9a, 0x63, 0x49, 0xe5, 0x42, 0xe4, 0x15, 0xb7,
    0xc8, 0x06, 0x70, 0x9d, 0x41, 0x75, 0x19, 0xc9, 0xaa, 0xfc, 0x4d, 0xbf, 0x2a, 0x73, 0x84, 0xd5,
    0xc3, 0xaf, 0x2b, 0x86, 0xa7, 0xb1, 0xb2, 0x5b, 0x46, 0xd3, 0x9f, 0xfd, 0xd4, 0x0f, 0x9c, 0x2f,
    0x9b, 0x43, 0xef, 0xd9, 0x79, 0xb6, 0x53, 0x7f, 0xc1, 0xf0, 0x23, 0xe7, 0x25, 0x5e, 0xb5, 0x1e,
    0xa2, 0xdf, 0xa6, 0xfe, 0xac, 0x22, 0xf9, 0xe2, 0x4a, 0xbc, 0x35, 0xca, 0xee, 0x78, 0x05, 0x6b,
    0x51, 0xe1, 0x59, 0xa3, 0xf2, 0x71, 0x56, 0x11, 0x6a, 0x89, 0x94, 0x65, 0x8c, 0xbb, 0x77, 0x3c,
    0x7b, 0x28, 0xab, 0xd2, 0x31, 0xde, 0xc4, 0x5f, 0xcc, 0xcf, 0x76, 0x2c, 0xb8, 0xd8, 0x2e, 0x36,
    0xdb, 0x69, 0xb3, 0x14, 0x95, 0xbe, 0x62, 0xa1, 0x3b, 0x16, 0x66, 0xe9, 0x5c, 0x6c, 0x6d, 0xad,
    0x37, 0x61, 0x4b, 0xb9, 0xe3, 0xba, 0xf1, 0xa0, 0x85, 0x83, 0xda, 0x47, 0xc5, 0xb0, 0x33, 0xfa,
    0x96, 0x6f, 0x6e, 0xc2, 0xf6, 0x50, 0xff, 0x5d, 0xa9, 0x8e, 0x17, 0x1b, 0x97, 0x7d, 0xec, 0x58,
    0xf7, 0x1f, 0xfb, 0x7c, 0x09, 0x0d, 0x7a, 0x67, 0x45, 0x87, 0xdc, 0xe8, 0x4f, 0x1d, 0x4e, 0x04,
    0xeb, 0xf8, 0xf3, 0x3e, 0x3d, 0xbd, 0x8a, 0x88, 0xdd, 0xcd, 0x0b, 0x13, 0x98, 0x02, 0x93, 0x80,
    0x90, 0xd0, 0x24, 0x34, 0xcb, 0xed, 0xf4, 0xce, 0x99, 0x10, 0x44, 0x40, 0x92, 0x3a, 0x01, 0x26,
    0x12, 0x1a, 0x48, 0x68, 0xf5, 0x81, 0x8b, 0xc7, 0xd6, 0x20, 0x0a, 0x08, 0x00, 0x4c, 0xd7, 0x74
]

_kB = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]


def _mul(a, b):
    p = 0
    while b:
        if b & 1:
            p ^= a
        b >>= 1
        a <<= 1
        if a & 0x100:
            a ^= 0x1C3
    return p


def _func_x(a, b):
    assert len(a) == 16 and len(b) == 16
    return bytearray([i ^ j for i, j in zip(a, b)])


def _func_s(a):
    return bytearray([_kpi[i] for i in a])


def _func_reverse_s(a):
    return bytearray([_reverse_kpi[i] for i in a])


def _func_lin(a):
    return bytearray([reduce(
        lambda acc, i: acc ^ i,
        [_mul(i, j) for i, j in zip(a, _kB)],
        0
    )])


def _func_r(a):
    return _func_lin(a) + a[:-1]


def _func_reverse_r(a):
    return a[1:] + _func_lin(a[1:] + a[0:1])


def _repeat_func(func, a):
    return reduce(
        lambda acc, f: f(acc),
        16 * [func],
        a
    )


def _func_l(a):
    return _repeat_func(_func_r, a)


def _func_reverse_l(a):
    return _repeat_func(_func_reverse_r, a)


def _func_lsx(a, b):
    return _func_l(_func_s(_func_x(a, b)))


def _func_reverse_lsx(a, b):
    return _func_reverse_s(_func_reverse_l(_func_x(a, b)))


def _func_f(k1, k2, c):
    return _func_x(_func_lsx(k1, c), k2), k1


def _func_c(n):
    a = bytearray(16)
    a[-1] = bytearray([n])[0]
    return _func_l(a)


def expand_key(master_key):
    keys = bytearray(160)
    keys[:32] = master_key[:]
    for i in range(4):
        n, m = 32 * i, 32 * (i + 1)
        k1, k2 = keys[n: n + 16], keys[n + 16: m]
        for j in range(1, 8):
            c = _func_c(8 * i + j)
            k1, k2 = _func_f(k1, k2, c)
        c = _func_c(8 * (i + 1))
        k1, k2 = _func_f(k1, k2, c)
        keys[m: m + 16] = k1
        keys[m + 16: m + 32] = k2
    return keys


def _encrypt_bytes16(plain_bytes16, keys):
    assert len(plain_bytes16) == 16
    cipher_text16 = plain_bytes16[:]
    for i in range(9):
        n, m = 16 * i, 16 * (i + 1)
        cipher_text16 = _func_lsx(cipher_text16, keys[n:m])
    return _func_x(cipher_text16, keys[16 * 9:])


def _decrypt_bytes16(cipher_bytes16, keys):
    assert len(cipher_bytes16) == 16
    plain_text16 = cipher_bytes16[:]
    for i in range(9):
        n, m = 16 * (9 - i), 16 * (9 - i + 1)
        plain_text16 = _func_reverse_lsx(plain_text16, keys[n:m])
    return _func_x(plain_text16, keys[:16])


def _chunks(bytes_):
    assert len(bytes_) % 16 == 0
    for i in range(0, len(bytes_), 16):
        yield bytes_[i: i + 16]


def encrypt_text(plain, keys):
    plain_bytes = bytes_func.from_str(plain)
    encrypted = map(lambda bytes16: _encrypt_bytes16(bytes16, keys), _chunks(plain_bytes))
    return reduce(lambda acc, bytes16: acc + bytes16, encrypted)


def decrypt_text(cipher, keys):
    decrypted = map(lambda bytes16: _decrypt_bytes16(bytes16, keys), _chunks(cipher))
    decrypted = reduce(lambda acc, bytes16: acc + bytes16, decrypted)
    return bytes_func.to_str(decrypted)


def test_bytes():
    master_key = bytearray.fromhex('8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef')
    keys = expand_key(master_key)
    expect_key = bytearray.fromhex('72e9dd7416bcf45b755dbaa88e4a4043')
    assert expect_key == keys[144:], f'keys\nexpect: {expect_key}\nkey 10: {keys[144:]}'

    plain_bytes = bytearray.fromhex('1122334455667700ffeeddccbbaa9988')
    expect_cipher = bytearray.fromhex('7f679d90bebc24305a468d42b9d4edcd')
    cipher_bytes = _encrypt_bytes16(plain_bytes, keys)
    assert expect_cipher == cipher_bytes, f'encrypt\nexpect: {expect_cipher}\ncipher: {cipher_bytes}'

    decrypted_bytes = _decrypt_bytes16(cipher_bytes, keys)
    assert decrypted_bytes == plain_bytes, f'decrypt\nexpect: {plain_bytes}\ndecrypt: {decrypted_bytes}'


def test_text():
    master_key = bytearray.fromhex('8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef')
    keys = expand_key(master_key)
    plain = 'Hello World!'
    cipher = encrypt_text(plain, keys)
    decrypted = decrypt_text(cipher, keys)
    assert plain == decrypted, f'\nexpect: {plain}\ndecrypt: {decrypted}'


if __name__ == '__main__':
    test_bytes()
    test_text()
