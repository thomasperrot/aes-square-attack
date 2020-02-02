import binascii
from functools import partial

import pytest

from aes.connectors import encrypt_delta_set
from aes.square import crack_last_key, get_delta_set, guess_position, is_guess_correct, reverse_state


@pytest.mark.slow
def test_crack_last_key():
    key = binascii.unhexlify("2b7e151628aed2a6abf7158809cf4f3c")
    get_encrypted_ds = partial(encrypt_delta_set, key)
    cracked_key = crack_last_key(get_encrypted_ds)
    assert cracked_key == binascii.unhexlify("ef44a541a8525b7fb671253bdb0bad00")


def test_guess_position():
    key = binascii.unhexlify("2b7e151628aed2a6abf7158809cf4f3c")
    ds_encrypter = partial(encrypt_delta_set, key)
    guess = guess_position(ds_encrypter, 0)
    assert guess == 239


@pytest.mark.parametrize(
    "byte_values, expected",
    [pytest.param(list(range(0x10)), True), pytest.param([i // 3 for i in range(0x10)], False)],
)
def test_is_guess_correct(byte_values, expected):
    assert is_guess_correct(byte_values) is expected


def test_get_delta_set():
    ds = get_delta_set(0xCC)
    for i in range(4):
        for j in range(4):
            for k in range(len(ds)):
                if (i, j) == (0, 0):
                    assert ds[k][i][j] == k
                else:
                    assert ds[k][i][j] == 0xCC


def test_reverse_square():
    key = binascii.unhexlify("2b7e151628aed2a6abf7158809cf4f3c")
    ds = get_delta_set(0xCC)
    encrypted_ds = encrypt_delta_set(key, ds)
    reversed_bytes = reverse_state(239, (0, 0), encrypted_ds)
    assert reversed_bytes == [
        37,
        124,
        32,
        153,
        80,
        41,
        37,
        225,
        245,
        223,
        31,
        19,
        160,
        205,
        37,
        77,
        153,
        92,
        37,
        86,
        202,
        42,
        227,
        103,
        175,
        139,
        149,
        156,
        201,
        201,
        59,
        147,
        36,
        120,
        26,
        37,
        87,
        187,
        139,
        86,
        183,
        179,
        221,
        127,
        123,
        213,
        44,
        236,
        80,
        28,
        94,
        205,
        206,
        173,
        51,
        81,
        63,
        85,
        22,
        23,
        90,
        232,
        234,
        104,
        233,
        241,
        1,
        250,
        231,
        10,
        96,
        141,
        178,
        108,
        45,
        136,
        243,
        40,
        144,
        154,
        205,
        170,
        241,
        128,
        161,
        96,
        167,
        118,
        250,
        129,
        153,
        29,
        223,
        35,
        162,
        75,
        24,
        189,
        197,
        100,
        44,
        205,
        94,
        126,
        53,
        46,
        162,
        66,
        35,
        178,
        197,
        42,
        58,
        214,
        118,
        35,
        126,
        82,
        186,
        60,
        82,
        100,
        90,
        194,
        7,
        176,
        166,
        166,
        126,
        42,
        147,
        109,
        53,
        153,
        20,
        72,
        136,
        65,
        181,
        91,
        194,
        71,
        170,
        249,
        41,
        73,
        254,
        164,
        231,
        15,
        63,
        88,
        8,
        190,
        242,
        34,
        248,
        195,
        45,
        232,
        158,
        16,
        123,
        153,
        170,
        237,
        166,
        19,
        216,
        152,
        7,
        55,
        236,
        184,
        102,
        33,
        215,
        254,
        147,
        197,
        229,
        174,
        191,
        92,
        246,
        223,
        119,
        240,
        232,
        80,
        196,
        82,
        116,
        126,
        6,
        80,
        194,
        57,
        78,
        194,
        80,
        8,
        167,
        170,
        79,
        97,
        219,
        62,
        36,
        91,
        100,
        16,
        223,
        107,
        225,
        8,
        66,
        84,
        42,
        72,
        110,
        183,
        250,
        12,
        191,
        227,
        99,
        56,
        197,
        52,
        106,
        242,
        73,
        133,
        243,
        125,
        20,
        76,
        225,
        230,
        134,
        111,
        170,
        46,
        128,
        60,
        134,
        138,
        233,
        0,
        160,
        192,
        7,
        63,
        119,
        37,
    ]
