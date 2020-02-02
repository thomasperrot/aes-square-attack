from typing import Iterable, List

from .aes import transform_state
from .common import State
from .square import SQUARE_ROUNDS


def encrypt_delta_set(key: bytes, delta_set: Iterable[State], rounds: int = SQUARE_ROUNDS) -> List[State]:
    return [transform_state(s, key, rounds=rounds) for s in delta_set]
