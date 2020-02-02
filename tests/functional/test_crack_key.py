import binascii
from functools import partial

import pytest

from aes.connectors import encrypt_delta_set
from aes.square import crack_key


@pytest.mark.slow
def test_crack_key():
    # given
    key = binascii.unhexlify("3d80477d4716fe3e1e237e446d7a883b")
    get_encrypted_ds = partial(encrypt_delta_set, key)

    # when
    cracked_key = crack_key(get_encrypted_ds)

    # then
    assert cracked_key == key
