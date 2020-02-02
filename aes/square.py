from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import Callable, Iterable, List, Tuple

import numpy as np

from .common import S_BOX, State
from .key_expension import get_first_key

SQUARE_ROUNDS = 4
REVERSED_S_BOX = {v: k for k, v in S_BOX.items()}


def crack_key(encrypt_ds: Callable[[Iterable[State]], List[State]], rounds: int = SQUARE_ROUNDS) -> bytes:
    last_key = crack_last_key(encrypt_ds)
    cracked_key = get_first_key(last_key, rounds + 1)
    return cracked_key


def crack_last_key(encrypt_ds: Callable[[Iterable[State]], List[State]]) -> bytes:
    last_bytes = [0] * 16
    positions = list(range(16))
    position_guesser = partial(guess_position, encrypt_ds)
    with ProcessPoolExecutor() as executor:
        for position, found_byte in zip(positions, executor.map(position_guesser, positions)):
            last_bytes[position] = found_byte
    return bytes(last_bytes)


def guess_position(encrypt_ds: Callable[[Iterable[State]], List[State]], position: int) -> int:
    position_in_state = (position % 4, position // 4)
    for inactive_value in range(0x100):
        ds = get_delta_set(inactive_value)
        encrypted_ds = encrypt_ds(ds)
        correct_guesses = []
        for guess in range(0x100):
            reversed_bytes = reverse_state(guess, position_in_state, encrypted_ds)
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


def get_delta_set(inactive_value: int) -> List[State]:
    base_state = np.full((4, 4), inactive_value)
    delta_set = []
    for i in range(256):
        state = base_state.copy()
        state[0, 0] = i
        delta_set.append(state)
    return delta_set
