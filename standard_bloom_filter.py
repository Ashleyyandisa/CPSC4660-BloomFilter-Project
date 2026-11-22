"""A basic Bloom filter using a bytearray and SHA-256 hashing."""

import hashlib

class StandardBloomFilter:
    """Store probable membership of items with a fixed-size bit array.

    Bloom filters can return false positives, but not false negatives for
    items that have been added (unless the filter is modified or reset).
    """

    def __init__(self, size: int, num_hashes: int):
        if size <= 0:
            raise ValueError("size must be greater than 0")
        if num_hashes <= 0:
            raise ValueError("num_hashes must be greater than 0")

        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bytearray((size + 7) // 8)

    def _hashes(self, item: str):
        """Generate repeatable bit positions for a string."""
        if not isinstance(item, str):
            raise TypeError("item must be a string")

        digest = hashlib.sha256(item.encode("utf-8")).digest()
        first = int.from_bytes(digest[:16], "big")
        second = int.from_bytes(digest[16:], "big") or 1

        for i in range(self.num_hashes):
            yield (first + i * second) % self.size

    def add(self, item: str) -> None:
        """Mark all hash positions for the item as present."""
        for position in self._hashes(item):
            byte_index, bit_index = divmod(position, 8)
            self.bit_array[byte_index] |= 1 << bit_index

    def contains(self, item: str) -> bool:
        """Return False if definitely absent, True if possibly present."""
        for position in self._hashes(item):
            byte_index, bit_index = divmod(position, 8)
            if not (self.bit_array[byte_index] & (1 << bit_index)):
                return False
        return True

    def __contains__(self, item: str) -> bool:
        return self.contains(item)