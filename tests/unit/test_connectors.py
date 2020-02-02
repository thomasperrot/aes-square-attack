import binascii
from functools import partial

from aes.connectors import encrypt_delta_set
from aes.square import get_delta_set


def test_get_encrypted_delta_set():
    key = binascii.unhexlify("2b7e151628aed2a6abf7158809cf4f3c")
    ds = get_delta_set(0xCC)
    delta_set_encrypter = partial(encrypt_delta_set, key, rounds=3)
    encrypted_delta_set = delta_set_encrypter(ds)
    for i in range(4):
        for j in range(4):
            r = 0
            for k in range(len(encrypted_delta_set)):
                r ^= encrypted_delta_set[k][i][j]
            assert r == 0
