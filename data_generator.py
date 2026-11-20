"""Reproducible random data for Bloom filter experiments."""

import random
import string


CHARACTERS = string.ascii_letters + string.digits
random_generator = random.Random(42)


def generate_random_string(length=12, rng=None):
    """Generate one random string containing letters and digits."""
    if type(length) is not int or length <= 0:
        raise ValueError("length must be a positive integer")

    if rng is None:
        rng = random_generator

    return "".join(rng.choice(CHARACTERS) for _ in range(length))


def generate_dataset(num_inserted, num_queries, seed=42):
    """Return two reproducible, non-overlapping lists of unique strings."""
    for name, count in (("num_inserted", num_inserted), ("num_queries", num_queries)):
        if type(count) is not int or count < 0:
            raise ValueError(f"{name} must be a non-negative integer")

    total = num_inserted + num_queries
    length = 12
    if total > len(CHARACTERS) ** length:
        raise ValueError("requested more unique strings than are possible")

    try:
        rng = random.Random(seed)
    except (TypeError, ValueError) as exc:
        raise ValueError("seed must be valid for random.Random") from exc

    strings = []  # Keep the generated order.
    seen = set()  # Check duplicates efficiently.

    while len(strings) < total:
        item = generate_random_string(length, rng)
        if item not in seen:
            seen.add(item)
            strings.append(item)

    inserted = strings[:num_inserted]
    queries = strings[num_inserted:]
    return inserted, queries
