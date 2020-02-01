import binascii

import pytest

from aes.square import _get_delta_set, get_encrypted_delta_set, is_guess_correct, reverse_state


@pytest.skip("TODO: make this test pass")
def test_reverse_square():
    key = binascii.unhexlify("2b7e151628aed2a6abf7158809cf4f3c")
    encrypted_ds = get_encrypted_delta_set(key)
    for guess in range(0x100):
        reversed_bytes = reverse_state(key[0], (0, 0), encrypted_ds)
        if is_guess_correct(reversed_bytes):
            break
    else:
        pytest.fail("No correct byte found...")


@pytest.mark.parametrize(
    "byte_values, expected",
    [pytest.param(list(range(0x10)), True), pytest.param([i // 3 for i in range(0x10)], False)],
)
def test_is_guess_correct(byte_values, expected):
    assert is_guess_correct(byte_values) is expected


def test_get_encrypted_delta_set():
    key = binascii.unhexlify("2b7e151628aed2a6abf7158809cf4f3c")
    encrypted_delta_set = get_encrypted_delta_set(key, rounds=3)
    for i in range(4):
        for j in range(4):
            r = 0
            for k in range(len(encrypted_delta_set)):
                r ^= encrypted_delta_set[k][i][j]
            assert r == 0


def test_get_delta_set():
    ds = _get_delta_set()
    inactive_value = ds[0][1][0]
    for i in range(4):
        for j in range(4):
            for k in range(len(ds)):
                if (i, j) == (0, 0):
                    assert ds[k][i][j] == k
                else:
                    assert ds[k][i][j] == inactive_value
