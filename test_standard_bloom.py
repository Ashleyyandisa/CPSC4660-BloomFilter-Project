"""Unit tests for the StandardBloomFilter implementation."""

import unittest

from standard_bloom_filter import StandardBloomFilter


class TestStandardBloomFilter(unittest.TestCase):
    def setUp(self):
        self.bloom = StandardBloomFilter(size=1000, num_hashes=3)

    def test_inserted_item_is_present(self):
        self.bloom.add("apple")
        self.assertTrue(self.bloom.contains("apple"))

    def test_empty_filter_rejects_item(self):
        self.assertFalse(self.bloom.contains("banana"))

    def test_multiple_inserted_items_are_present(self):
        items = ["apple", "banana", "orange"]
        for item in items:
            self.bloom.add(item)
        for item in items:
            with self.subTest(item=item):
                self.assertTrue(self.bloom.contains(item))

    def test_duplicate_insertion_does_not_change_bits(self):
        self.bloom.add("apple")
        before = bytes(self.bloom.bit_array)
        self.bloom.add("apple")
        self.assertEqual(bytes(self.bloom.bit_array), before)

    def test_invalid_filter_parameters(self):
        for size, hashes in [(0, 3), (-10, 3), (1000, 0), (1000, -2)]:
            with self.subTest(size=size, num_hashes=hashes):
                with self.assertRaises(ValueError):
                    StandardBloomFilter(size=size, num_hashes=hashes)

    def test_non_string_items_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.bloom.add(12345)
        with self.assertRaises(TypeError):
            self.bloom.contains(12345)

    def test_in_operator(self):
        self.bloom.add("apple")
        self.assertIn("apple", self.bloom)

    def test_storage_size_in_bytes(self):
        bloom = StandardBloomFilter(size=10, num_hashes=2)
        self.assertEqual(len(bloom.bit_array), 2)

    def test_no_false_negatives_after_many_insertions(self):
        items = [f"item-{i}" for i in range(200)]
        for item in items:
            self.bloom.add(item)
        for item in items:
            with self.subTest(item=item):
                self.assertTrue(self.bloom.contains(item))


if __name__ == "__main__":
    unittest.main()
