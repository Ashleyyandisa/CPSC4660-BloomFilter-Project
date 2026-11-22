import random
import string
import unittest

from data_generator import generate_dataset, generate_random_string


class TestDataGenerator(unittest.TestCase):
    def test_default_string_length(self):
        self.assertEqual(len(generate_random_string()), 12)

    def test_custom_string_length_and_characters(self):
        value = generate_random_string(24, rng=random.Random(7))
        self.assertEqual(len(value), 24)
        self.assertTrue(all(char in string.ascii_letters + string.digits for char in value))

    def test_random_string_length_validation(self):
        for length in (0, -1, 2.5, True, "12"):
            with self.subTest(length=length):
                with self.assertRaises(ValueError):
                    generate_random_string(length)

    def test_dataset_sizes(self):
        inserted, queries = generate_dataset(1000, 500)
        self.assertEqual(len(inserted), 1000)
        self.assertEqual(len(queries), 500)

    def test_all_items_unique_and_non_overlapping(self):
        inserted, queries = generate_dataset(2000, 2000)
        self.assertEqual(len(set(inserted)), len(inserted))
        self.assertEqual(len(set(queries)), len(queries))
        self.assertTrue(set(inserted).isdisjoint(queries))

    def test_all_generated_items_are_twelve_character_strings(self):
        inserted, queries = generate_dataset(20, 20)
        for item in inserted + queries:
            with self.subTest(item=item):
                self.assertIsInstance(item, str)
                self.assertEqual(len(item), 12)

    def test_same_seed_reproduces_same_lists(self):
        self.assertEqual(generate_dataset(100, 100, seed=42),
                         generate_dataset(100, 100, seed=42))

    def test_different_seeds_change_dataset(self):
        self.assertNotEqual(generate_dataset(100, 100, seed=42),
                            generate_dataset(100, 100, seed=99))

    def test_zero_counts(self):
        self.assertEqual(generate_dataset(0, 0), ([], []))
        self.assertEqual(generate_dataset(0, 3)[0], [])
        self.assertEqual(generate_dataset(3, 0)[1], [])

    def test_invalid_counts(self):
        for inserted, queries in ((-1, 5), (5, -1), (1.5, 2), (True, 2), (2, "4")):
            with self.subTest(inserted=inserted, queries=queries):
                with self.assertRaises(ValueError):
                    generate_dataset(inserted, queries)

    def test_invalid_seed(self):
        with self.assertRaises(ValueError):
            generate_dataset(5, 5, seed=[])


if __name__ == "__main__":
    unittest.main()