import math
import hashlib


class BloomFilter:
    def __init__(self, capacity, error_rate):
        self.capacity = capacity
        self.error_rate = error_rate
        self.count = 0

        # Calculate bit array size
        self.size = math.ceil(
            -(capacity * math.log(error_rate)) / (math.log(2) ** 2)
        )

        # Calculate number of hash functions
        self.num_hashes = max(
            1,
            round((self.size / capacity) * math.log(2))
        )

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


class ScalableBloomFilter:
    def __init__(
        self,
        initial_capacity=1000,
        error_rate=0.01,
        growth_factor=2,
        tightening_ratio=0.8
    ):
        self.initial_capacity = initial_capacity
        self.error_rate = error_rate
        self.growth_factor = growth_factor
        self.tightening_ratio = tightening_ratio

        self.filters = []

        self._add_new_filter()

    def _add_new_filter(self):
        filter_number = len(self.filters)

        # Capacity increases geometrically
        new_capacity = int(
            self.initial_capacity *
            (self.growth_factor ** filter_number)
        )

        # Each new filter gets a smaller error probability
        new_error_rate = (
            self.error_rate *
            (1 - self.tightening_ratio) *
            (self.tightening_ratio ** filter_number)
        )

        new_filter = BloomFilter(
            capacity=new_capacity,
            error_rate=new_error_rate
        )

        self.filters.append(new_filter)

    def add(self, item):
        current_filter = self.filters[-1]

        # If current filter is full, create another filter
        if current_filter.count >= current_filter.capacity:
            self._add_new_filter()
            current_filter = self.filters[-1]

        current_filter.add(item)

    def contains(self, item):
        # Search newest filter first
        for bloom_filter in reversed(self.filters):
            if bloom_filter.contains(item):
                return True

        return False

    def memory_bits(self):
        return sum(
            bloom_filter.memory_bits()
            for bloom_filter in self.filters
        )

    def number_of_filters(self):
        return len(self.filters)