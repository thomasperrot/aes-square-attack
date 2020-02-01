import binascii
from functools import partial

import pytest

from aes.key_expension import get_first_key
from aes.square import crack_last_key, get_encrypted_delta_set


@pytest.mark.slow
def test_crack_key():
    # given
    key = binascii.unhexlify("3d80477d4716fe3e1e237e446d7a883b")
    rounds = 4
    get_encrypted_ds = partial(get_encrypted_delta_set, key)

    # when
    last_key = crack_last_key(get_encrypted_ds)
    cracked_key = get_first_key(last_key, rounds + 1)

    # then
    assert cracked_key == key
