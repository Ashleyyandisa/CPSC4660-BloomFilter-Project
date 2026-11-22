import csv
import os
import matplotlib.pyplot as plt


RESULTS_FILE = "results/results.csv"


def load_results():
    rows = []

    with open(RESULTS_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            rows.append({
                "dataset_size": int(row["dataset_size"]),

                "standard_fpr": float(row["standard_fpr"]) * 100,
                "scalable_fpr": float(row["scalable_fpr"]) * 100,

                "standard_memory_bits":
                    int(row["standard_memory_bits"]),
                "scalable_memory_bits":
                    int(row["scalable_memory_bits"]),

                "standard_insertion_time":
                    float(row["standard_insertion_time"]),
                "scalable_insertion_time":
                    float(row["scalable_insertion_time"]),

                "standard_lookup_time":
                    float(row["standard_lookup_time"]),
                "scalable_lookup_time":
                    float(row["scalable_lookup_time"])
            })

    return rows


def save_graph(x, standard, scalable, title, ylabel, filename):
    plt.figure()

    plt.plot(x, standard, marker="o", label="Standard Bloom Filter")
    plt.plot(x, scalable, marker="o", label="Scalable Bloom Filter")

    plt.xlabel("Number of Inserted Items")
    plt.ylabel(ylabel)
    plt.title(title)

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"results/{filename}")
    plt.close()


def main():
    os.makedirs("results", exist_ok=True)

    rows = load_results()

    sizes = [row["dataset_size"] for row in rows]

    # Graph 1: False-positive rate
    save_graph(
        sizes,
        [row["standard_fpr"] for row in rows],
        [row["scalable_fpr"] for row in rows],
        "False-Positive Rate vs Dataset Size",
        "False-Positive Rate (%)",
        "false_positive_rate.png"
    )

    # Graph 2: Memory usage
    save_graph(
        sizes,
        [row["standard_memory_bits"] for row in rows],
        [row["scalable_memory_bits"] for row in rows],
        "Memory Usage vs Dataset Size",
        "Memory Usage (bits)",
        "memory_usage.png"
    )

    # Graph 3: Insertion time
    save_graph(
        sizes,
        [row["standard_insertion_time"] for row in rows],
        [row["scalable_insertion_time"] for row in rows],
        "Insertion Time vs Dataset Size",
        "Insertion Time (seconds)",
        "insertion_time.png"
    )

    # Graph 4: Lookup time
    save_graph(
        sizes,
        [row["standard_lookup_time"] for row in rows],
        [row["scalable_lookup_time"] for row in rows],
        "Lookup Time vs Dataset Size",
        "Lookup Time (seconds)",
        "lookup_time.png"
    )

    print("Graphs created successfully:")
    print("results/false_positive_rate.png")
    print("results/memory_usage.png")
    print("results/insertion_time.png")
    print("results/lookup_time.png")


if __name__ == "__main__":
    main()