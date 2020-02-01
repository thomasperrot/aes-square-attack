from typing import Callable, Iterable, List, Tuple

import numpy as np

from .aes import transform_state
from .common import S_BOX, State

SQUARE_ROUNDS = 4
REVERSED_S_BOX = {v: k for k, v in S_BOX.items()}


def crack_last_key(get_encrypted_ds: Callable) -> bytes:
    last_bytes = []
    for position in range(16):
        b = guess_position(position, get_encrypted_ds)
        last_bytes.append(b)
    return bytes(last_bytes)


def guess_position(position: int, get_encrypted_ds: Callable) -> int:
    position_in_state = (position % 4, position // 4)
    for inactive_value in range(0x100):
        ds = get_encrypted_ds(inactive_value)
        correct_guesses = []
        for guess in range(0x100):
            reversed_bytes = reverse_state(guess, position_in_state, ds)
            if is_guess_correct(reversed_bytes):
                correct_guesses.append(guess)
        if len(correct_guesses) == 1:
            break
    else:
        raise RuntimeError(f"Could not find byte for position {position}")
    return correct_guesses[0]


def reverse_state(guess: int, position: Tuple[int, int], encrypted_ds: Iterable[State]) -> List[int]:
    r = []
    i, j = position
    for s in encrypted_ds:
        before_add_round_key = s[i, j] ^ guess
        before_sub_byte = REVERSED_S_BOX[before_add_round_key]
        r.append(before_sub_byte)
    return r


def is_guess_correct(reversed_bytes: Iterable[int]) -> bool:
    r = 0
    for i in reversed_bytes:
        r ^= i
    return r == 0


def get_encrypted_delta_set(key: bytes, inactive_value: int, rounds: int = SQUARE_ROUNDS) -> List[State]:
    delta_set = _get_delta_set(inactive_value)
    return [transform_state(s, key, rounds=rounds) for s in delta_set]


def _get_delta_set(inactive_value: int) -> List[State]:
    base_state = np.full((4, 4), inactive_value)
    delta_set = []
    for i in range(256):
        state = base_state.copy()
        state[0, 0] = i
        delta_set.append(state)
    return delta_set
