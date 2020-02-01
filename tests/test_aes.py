import binascii

import numpy as np

from aes.aes import _add_round_key, _mix_columns, _shift_rows, _sub_bytes, encrypt, transform_state


def test_encrypt():
    """Testing using example in https://csrc.nist.gov/csrc/media/publications/fips/197/final/documents/fips-197.pdf,
    page 35."""

    key = binascii.unhexlify("000102030405060708090a0b0c0d0e0f")
    plain_text = binascii.unhexlify("00112233445566778899aabbccddeeff")
    assert encrypt(plain_text, key) == binascii.unhexlify("69c4e0d86a7b0430d8cdb78070b4c55a")


def test_transform_state():
    key = binascii.unhexlify("2b7e151628aed2a6abf7158809cf4f3c")
    plain_text = "theblockbreakers".encode()
    state = np.array(list(plain_text), dtype=int)
    state = np.reshape(state, (4, 4), order="F")
    final_state = transform_state(state, key)
    assert np.array_equal(
        final_state,
        np.array(
            [[0xC6, 0x02, 0x23, 0x2F], [0x9F, 0x5A, 0x93, 0x05], [0x25, 0x9E, 0xF6, 0xB7], [0xD0, 0xF3, 0x3E, 0x47]]
        ),
    )


def test_sub_bytes():
    state = np.arange(0, 0x10)
    state = np.reshape(state, (4, 4), order="F")
    new_state = _sub_bytes(state)
    assert np.array_equal(
        new_state,
        np.array(
            [[0x63, 0xF2, 0x30, 0xFE], [0x7C, 0x6B, 0x01, 0xD7], [0x77, 0x6F, 0x67, 0xAB], [0x7B, 0xC5, 0x2B, 0x76]]
        ),
    )


def test_shift_rows():
    state = np.array(
        [[0x63, 0xF2, 0x30, 0xFE], [0x7C, 0x6B, 0x01, 0xD7], [0x77, 0x6F, 0x67, 0xAB], [0x7B, 0xC5, 0x2B, 0x76]]
    )
    new_state = _shift_rows(state)
    assert np.array_equal(
        new_state,
        np.array(
            [[0x63, 0xF2, 0x30, 0xFE], [0x6B, 0x01, 0xD7, 0x7C], [0x67, 0xAB, 0x77, 0x6F], [0x76, 0x7B, 0xC5, 0x2B]]
        ),
    )


def test_mix_columns():
    state = np.array(
        [[0x63, 0xF2, 0x30, 0xFE], [0x6B, 0x01, 0xD7, 0x7C], [0x67, 0xAB, 0x77, 0x6F], [0x76, 0x7B, 0xC5, 0x2B]]
    )
    new_state = _mix_columns(state)
    assert np.array_equal(
        new_state,
        np.array(
            [[0x6A, 0x2C, 0xB0, 0x27], [0x6A, 0x6D, 0xD9, 0x9C], [0x5C, 0x33, 0x5D, 0x21], [0x45, 0x51, 0x61, 0x5C]]
        ),
    )


def test_add_round_key():
    state = np.array(
        [[0x6A, 0x2C, 0xB0, 0x27], [0x6A, 0x6D, 0xD9, 0x9C], [0x5C, 0x33, 0x5D, 0x21], [0x45, 0x51, 0x61, 0x5C]]
    )
    key = [
        b"\xd6\xaa\x74\xfd",
        b"\xd2\xaf\x72\xfa",
        b"\xda\xa6\x78\xf1",
        b"\xd6\xab\x76\xfe",
    ]
    new_state = _add_round_key(state, key)
    assert np.array_equal(
        new_state,
        np.array(
            [[0xBC, 0xFE, 0x6A, 0xF1], [0xC0, 0xC2, 0x7F, 0x37], [0x28, 0x41, 0x25, 0x57], [0xB8, 0xAB, 0x90, 0xA2]]
        ),
    )
