import random
from typing import List, Tuple

import numpy as np

from .aes import transform_state
from .common import S_BOX, State

SQUARE_ROUNDS = 4
REVERSED_S_BOX = {v: k for k, v in S_BOX.items()}


def reverse_state(guess: int, position: Tuple[int, int], encrypted_ds: List[State]) -> List[int]:
    r = []
    i, j = position
    for s in encrypted_ds:
        before_add_round_key = s[i, j] ^ guess
        before_shift_rows = before_add_round_key  # TODO: maybe do something here
        before_sub_byte = REVERSED_S_BOX[before_shift_rows]
        r.append(before_sub_byte)
    return r


def is_guess_correct(delta_bytes: List[int]) -> bool:
    r = 0
    for i in delta_bytes:
        r ^= i
    return r == 0


def get_encrypted_delta_set(key: bytes, rounds: int = SQUARE_ROUNDS) -> List[State]:
    delta_set = _get_delta_set()
    return [transform_state(s, key, rounds=rounds) for s in delta_set]


def _get_delta_set() -> List[State]:
    base_state = np.full((4, 4), random.randint(0, 255))
    delta_set = []
    for i in range(256):
        state = base_state.copy()
        state[0, 0] = i
        delta_set.append(state)
    return delta_set
