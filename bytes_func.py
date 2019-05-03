import math


def print_bytes(bs):
    print([int(b) for b in bs])


def from_int(x):
    return bytearray(x.to_bytes((x.bit_length() + 7) // 8, 'big'))


def from_str(s):
    s = bytearray(s.encode())
    length = len(s).to_bytes(2, 'big')
    block_n = math.ceil((len(s) + 2) / 16)
    zeros = bytearray(16 * block_n - (len(s) + 2))
    return length + s + zeros


def to_str(b):
    length = int.from_bytes(b[:2], 'big')
    return b[2: 2 + length].decode()
