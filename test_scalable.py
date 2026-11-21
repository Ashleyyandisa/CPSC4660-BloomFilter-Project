from scalable_bloom_filter import ScalableBloomFilter


sbf = ScalableBloomFilter(
    initial_capacity=3,
    error_rate=0.01,
    growth_factor=2,
    tightening_ratio=0.8
)

items = ["apple", "banana", "orange", "grape", "mango"]

for item in items:
    sbf.add(item)
    print(
        f"Added {item}: "
        f"{sbf.number_of_filters()} filter(s)"
    )


print("\nMembership tests:")

for item in items:
    print(item, sbf.contains(item))


print("\nItem not inserted:")
print("watermelon", sbf.contains("watermelon"))


print("\nTotal filters:", sbf.number_of_filters())
print("Memory in bits:", sbf.memory_bits())