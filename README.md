# CPSC 4660 Bloom Filter Project

## Project Overview

This project compares a Standard Bloom Filter with a Scalable Bloom Filter based on the paper *Scalable Bloom Filters* by Almeida et al.

Bloom filters are probabilistic data structures used for fast membership testing. They can determine that an item is definitely not present or possibly present. They may produce false positives, but they do not produce false negatives for inserted items.

A Standard Bloom Filter has a fixed size and is designed for an expected number of items. If too many items are inserted, its false-positive rate can increase significantly.

A Scalable Bloom Filter solves this problem by adding additional Bloom filters as the dataset grows.

## Project Objectives

The project evaluates both implementations using:

- False-positive rate
- Memory usage
- Insertion time
- Lookup time
- Behaviour when the Standard Bloom Filter exceeds its intended capacity

The experiments use datasets of:

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
Implements the fixed-size Standard Bloom Filter.

`scalable_bloom_filter.py`  
Implements the Scalable Bloom Filter. New filters are created as the dataset grows.

`data_generator.py`  
Generates reproducible, unique, and non-overlapping datasets for insertion and false-positive testing.

`experiments.py`  
Runs the performance experiments and saves results to a CSV file.

`generate_graphs.py`  
Creates graphs from the experimental results.

`test_standard.py`  
Basic correctness test for the Standard Bloom Filter.

`test_scalable.py`  
Basic correctness and expansion test for the Scalable Bloom Filter.

`results/results.csv`  
Contains the recorded experimental results.

## How to Run

Install the required package:

```bash
python3 -m pip install -r requirements.txt
```

Run the basic tests:

```bash
python3 test_standard.py
python3 test_scalable.py
```

Run the full experiments:

```bash
python3 experiments.py
```

Generate the graphs:

```bash
python3 generate_graphs.py
```

## Performance Evaluation

The Standard Bloom Filter was configured for an expected capacity of 10,000 items.

| Dataset Size | Standard FPR | Scalable FPR |
|---:|---:|---:|
| 1,000 | 0.00% | 0.22% |
| 5,000 | 0.05% | 0.38% |
| 10,000 | 0.89% | 0.61% |
| 50,000 | 83.20% | 0.65% |
| 100,000 | 99.38% | 0.59% |

The Standard Bloom Filter performs well while the number of inserted items remains close to its intended capacity. Once the filter is heavily overloaded, its false-positive rate increases sharply.

The Scalable Bloom Filter maintains a low false-positive rate as the dataset grows because it creates additional filters instead of continuing to overload one fixed filter.

This comes with a trade-off. The Scalable Bloom Filter uses more memory and has higher insertion and lookup times because it maintains multiple filters.

## Results

The generated graphs are stored in the `results` directory:

- `false_positive_rate.png`
- `memory_usage.png`
- `insertion_time.png`
- `lookup_time.png`

## Contributors

- Abdul-Rahaman Safiu
- Ashley Ndebele

## Reference

Almeida, P. S., Baquero, C., Preguiça, N., & Hutchison, D. (2007). *Scalable Bloom Filters*. Information Processing Letters, 101(6), 255–261.