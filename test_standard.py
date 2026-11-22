from standard_bloom_filter import StandardBloomFilter


bf = StandardBloomFilter(
    capacity=3,
    error_rate=0.01
)

items = ["apple", "banana", "orange"]

for item in items:
    bf.add(item)


print("Membership tests:")

for item in items:
    print(item, bf.contains(item))


print("\nItem not inserted:")
print("watermelon", bf.contains("watermelon"))

print("\nInserted items:", bf.count)
print("Capacity:", bf.capacity)
print("Memory in bits:", bf.memory_bits())