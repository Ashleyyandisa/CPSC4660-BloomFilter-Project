"""Unit tests for the ScalableBloomFilter implementation."""

import unittest

from scalable_bloom_filter import ScalableBloomFilter


class TestScalableBloomFilter(unittest.TestCase):

    def setUp(self):
        self.bloom = ScalableBloomFilter(
            initial_capacity=10,
            error_rate=0.01,
            growth_factor=2,
            tightening_ratio=0.8
        )

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

    def test_new_filter_created_when_capacity_exceeded(self):
        initial_filters = self.bloom.number_of_filters()

        for i in range(11):
            self.bloom.add(f"item-{i}")

        self.assertGreater(
            self.bloom.number_of_filters(),
            initial_filters
        )

    def test_no_false_negatives_after_expansion(self):
        items = [f"item-{i}" for i in range(100)]

        for item in items:
            self.bloom.add(item)

        for item in items:
            with self.subTest(item=item):
                self.assertTrue(self.bloom.contains(item))

    def test_memory_increases_when_filter_expands(self):
        initial_memory = self.bloom.memory_bits()

        for i in range(11):
            self.bloom.add(f"item-{i}")

        self.assertGreater(
            self.bloom.memory_bits(),
            initial_memory
        )

    def test_initial_filter_count(self):
        self.assertEqual(
            self.bloom.number_of_filters(),
            1
        )


if __name__ == "__main__":
    unittest.main()