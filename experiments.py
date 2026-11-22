import csv
import os
import time

from data_generator import generate_dataset
from standard_bloom_filter import StandardBloomFilter
from scalable_bloom_filter import ScalableBloomFilter


DATASET_SIZES = [1000, 5000, 10000, 50000, 100000]
QUERY_COUNT = 10000
ERROR_RATE = 0.01
STANDARD_CAPACITY = 10000


def false_positive_rate(bloom_filter, queries):
    false_positives = 0

    for item in queries:
        if bloom_filter.contains(item):
            false_positives += 1

    return false_positives / len(queries)


def measure_lookup_time(bloom_filter, queries):
    start = time.perf_counter()

    for item in queries:
        bloom_filter.contains(item)

    end = time.perf_counter()

    return end - start


def run_standard(inserted, queries):
    bloom_filter = StandardBloomFilter(
        capacity=STANDARD_CAPACITY,
        error_rate=ERROR_RATE
    )

    start = time.perf_counter()

    for item in inserted:
        bloom_filter.add(item)

    insertion_time = time.perf_counter() - start

    fpr = false_positive_rate(bloom_filter, queries)
    lookup_time = measure_lookup_time(bloom_filter, queries)

    return {
        "fpr": fpr,
        "memory_bits": bloom_filter.memory_bits(),
        "insertion_time": insertion_time,
        "lookup_time": lookup_time
    }


def run_scalable(inserted, queries):
    bloom_filter = ScalableBloomFilter(
        initial_capacity=1000,
        error_rate=ERROR_RATE,
        growth_factor=2,
        tightening_ratio=0.8
    )

    start = time.perf_counter()

    for item in inserted:
        bloom_filter.add(item)

    insertion_time = time.perf_counter() - start

    fpr = false_positive_rate(bloom_filter, queries)
    lookup_time = measure_lookup_time(bloom_filter, queries)

    return {
        "fpr": fpr,
        "memory_bits": bloom_filter.memory_bits(),
        "insertion_time": insertion_time,
        "lookup_time": lookup_time,
        "num_filters": bloom_filter.number_of_filters()
    }


def main():
    os.makedirs("results", exist_ok=True)

    rows = []

    for size in DATASET_SIZES:
        print(f"\nRunning experiment for {size} inserted items...")

        inserted, queries = generate_dataset(
            num_inserted=size,
            num_queries=QUERY_COUNT,
            seed=42
        )

        standard = run_standard(inserted, queries)
        scalable = run_scalable(inserted, queries)

        print("Standard:", standard)
        print("Scalable:", scalable)

        rows.append({
            "dataset_size": size,

            "standard_fpr": standard["fpr"],
            "scalable_fpr": scalable["fpr"],

            "standard_memory_bits": standard["memory_bits"],
            "scalable_memory_bits": scalable["memory_bits"],

            "standard_insertion_time": standard["insertion_time"],
            "scalable_insertion_time": scalable["insertion_time"],

            "standard_lookup_time": standard["lookup_time"],
            "scalable_lookup_time": scalable["lookup_time"],

            "scalable_num_filters": scalable["num_filters"]
        })

    output_file = "results/results.csv"

    with open(output_file, "w", newline="") as csvfile:
        fieldnames = rows[0].keys()

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    main()