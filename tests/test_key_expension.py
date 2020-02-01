import binascii

import pytest

from aes.key_expension import _sub_word, key_expension


@pytest.mark.parametrize(
    "word, expected",
    [
        pytest.param(b"\x01\x00\x00\x00", b"\x7cccc"),
        pytest.param(b"\x00\xc2\x00\x00", b"c\x25cc"),
        pytest.param(b"\x00\x00\x9e\x00", b"cc\x0bc"),
    ],
)
def test_sub_word(word, expected):
    assert _sub_word(word) == expected


def test_key_expension():
    key = binascii.unhexlify("2b7e151628aed2a6abf7158809cf4f3c")
    words = key_expension(key, rounds=11)
    generated_keys = [b"".join(words[i : i + 4]) for i in range(0, len(words), 4)]
    print(generated_keys)
    assert generated_keys == [
        binascii.unhexlify(k)
        for k in [
            "2b7e151628aed2a6abf7158809cf4f3c",
            "a0fafe1788542cb123a339392a6c7605",
            "f2c295f27a96b9435935807a7359f67f",
            "3d80477d4716fe3e1e237e446d7a883b",
            "ef44a541a8525b7fb671253bdb0bad00",
            "d4d1c6f87c839d87caf2b8bc11f915bc",
            "6d88a37a110b3efddbf98641ca0093fd",
            "4e54f70e5f5fc9f384a64fb24ea6dc4f",
            "ead27321b58dbad2312bf5607f8d292f",
            "ac7766f319fadc2128d12941575c006e",
            "d014f9a8c9ee2589e13f0cc8b6630ca6",
        ]
    ]
