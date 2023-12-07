"""Utilities."""
from __future__ import annotations

import random


def sample_cards(size: int) -> [int]:
    """Sample random cards with size."""
    return random.sample(range(52), k=size)
