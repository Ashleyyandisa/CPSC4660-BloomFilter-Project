import math
import hashlib


class StandardBloomFilter:
    def __init__(self, capacity=1000, error_rate=0.01):
        self.capacity = capacity
        self.error_rate = error_rate
        self.count = 0

        # Number of bits needed
        self.size = math.ceil(
            -(capacity * math.log(error_rate)) / (math.log(2) ** 2)
        )

        # Number of hash functions
        self.num_hashes = max(
            1,
            round((self.size / capacity) * math.log(2))
        )

        # Bit array
        self.bit_array = [0] * self.size

    def _hashes(self, item):
        item = str(item)

        for i in range(self.num_hashes):
            value = f"{i}-{item}".encode()
            digest = hashlib.sha256(value).hexdigest()
            position = int(digest, 16) % self.size

            yield position

    def add(self, item):
        for position in self._hashes(item):
            self.bit_array[position] = 1

        self.count += 1

    def contains(self, item):
        for position in self._hashes(item):
            if self.bit_array[position] == 0:
                return False

        return True

    def memory_bits(self):
        return self.size