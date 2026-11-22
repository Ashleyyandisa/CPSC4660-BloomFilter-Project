# CPSC 4660 Bloom Filter Project

## Project Overview

This project compares a Standard Bloom Filter with a Scalable Bloom Filter based on the paper *Scalable Bloom Filters* by Almeida et al.

Bloom filters are probabilistic data structures used for fast membership testing. They can determine that an item is definitely not present or possibly present. Bloom filters may produce false positives, but they do not produce false negatives for items that have been inserted.

A Standard Bloom Filter has a fixed amount of memory and is normally designed for an expected number of items. If significantly more items are inserted than the filter was designed for, its false-positive rate can increase.

A Scalable Bloom Filter addresses this limitation by creating additional Bloom filters as the number of stored items increases.

## Project Objectives

The project evaluates the Standard Bloom Filter and Scalable Bloom Filter using:

- False-positive rate
- Memory usage
- Insertion time
- Lookup time
- Behaviour when the Standard Bloom Filter exceeds its intended capacity

The experiments use datasets containing:

- 1,000 items
- 5,000 items
- 10,000 items
- 50,000 items
- 100,000 items

## Technologies Used

- Python 3
- Matplotlib
- Git and GitHub
- VS Code

## Project Structure

`standard_bloom_filter.py`  
Implements the fixed-size Standard Bloom Filter using a packed bytearray and SHA-256-based double hashing.

`scalable_bloom_filter.py`  
Implements the Scalable Bloom Filter. New Bloom filters are created as the number of inserted items grows.

`data_generator.py`  
Generates reproducible, unique, and non-overlapping strings for insertion and query testing.

`experiments.py`  
Runs the performance experiments for both Bloom Filter implementations and saves the measurements to a CSV file.

`generate_graphs.py`  
Reads the experiment results and generates the four performance graphs.

`test_standard_bloom.py`  
Contains unit tests for the Standard Bloom Filter implementation.

`test_data_generator.py`  
Contains unit tests for the reproducible data generator.

`test_scalable.py`  
Tests the Scalable Bloom Filter's membership operations and verifies that additional filters are created when necessary.

`results/results.csv`  
Stores the experimental measurements for all dataset sizes.

`requirements.txt`  
Contains the external Python package required to generate the graphs.

## How to Run

Install the required package:

```bash
python3 -m pip install -r requirements.txt
```

Run the Standard Bloom Filter tests:

```bash
python3 test_standard_bloom.py
```

Run the data generator tests:

```bash
python3 test_data_generator.py
```

Run the Scalable Bloom Filter test:

```bash
python3 test_scalable.py
```

Run the complete experiments:

```bash
python3 experiments.py
```

Generate the graphs:

```bash
python3 generate_graphs.py
```

## Experiment Configuration

The Standard Bloom Filter was designed for an expected capacity of 10,000 items and a target false-positive rate of 1%.

The required bit-array size and number of hash functions are calculated from the expected capacity and target error rate before creating the Standard Bloom Filter.

The Scalable Bloom Filter was configured with:

- Initial capacity: 1,000 items
- Target error rate: 1%
- Growth factor: 2
- Tightening ratio: 0.8

For every dataset size, 10,000 non-inserted query items were used to measure the false-positive rate.

The same reproducible dataset generator and random seed were used throughout the experiments.

## Performance Evaluation

### False-Positive Rate

| Dataset Size | Standard FPR | Scalable FPR |
|---:|---:|---:|
| 1,000 | 0.00% | 0.22% |
| 5,000 | 0.03% | 0.38% |
| 10,000 | 1.19% | 0.61% |
| 50,000 | 83.80% | 0.65% |
| 100,000 | 99.58% | 0.59% |

The Standard Bloom Filter performs well while the number of inserted items remains within or close to its intended capacity.

At 10,000 inserted items, its measured false-positive rate was approximately 1.19%, which is close to its target value of 1%.

However, when the filter was heavily overloaded, the false-positive rate increased dramatically. At 50,000 inserted items it reached 83.80%, and at 100,000 items it reached 99.58%.

The Scalable Bloom Filter maintained a false-positive rate below 1% for every tested dataset size. At 100,000 inserted items, its false-positive rate was approximately 0.59%.

### Memory Usage

The Standard Bloom Filter uses a fixed-size bit array and therefore keeps approximately the same memory allocation throughout the experiments. Its allocated size was 95,856 bits.

The Scalable Bloom Filter increases its memory usage as the dataset grows because additional Bloom filters are created.

At 100,000 inserted items, the Scalable Bloom Filter contained seven internal filters and used approximately 1,940,907 bits.

### Insertion and Lookup Time

The Standard Bloom Filter generally required less insertion time because every item is inserted into a single fixed filter.

The Scalable Bloom Filter required more insertion time as the dataset increased because it manages several filters with different capacities and error probabilities.

Lookup operations were also generally slower for the Scalable Bloom Filter. A query that is not present may need to be checked against several internal Bloom filters before the structure can return `False`.

This demonstrates the main trade-off of the Scalable Bloom Filter. It requires additional memory and processing time, but it maintains a controlled false-positive rate when the number of stored elements grows beyond the original expected capacity.

## Results

The generated graphs are stored in the `results` directory:

- `false_positive_rate.png`
- `memory_usage.png`
- `insertion_time.png`
- `lookup_time.png`

The raw experiment measurements are stored in:

- `results/results.csv`

## Contributors

- Abdul-Rahaman Safiu
- Ashley Ndebele

## Reference

Almeida, P. S., Baquero, C., Preguiça, N., & Hutchison, D. (2007). *Scalable Bloom Filters*. Information Processing Letters, 101(6), 255–261.