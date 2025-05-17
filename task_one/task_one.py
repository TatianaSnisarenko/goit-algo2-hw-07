import random
import timeit
from query_processor import QueryProcessor

ARRAY_SIZE = 100_000
QUERY_COUNT = 50_000
CACHE_SIZE = 1000

# Initialize the array and cache
array = [random.randint(1, 100) for _ in range(ARRAY_SIZE)]
processor = QueryProcessor(array, CACHE_SIZE)

queries = []
for _ in range(QUERY_COUNT):
    if random.random() < 0.9:
        if queries:
            queries.append(queries[random.randint(0, len(queries) - 1)])
        else:
            left = random.randint(0, ARRAY_SIZE - 1)
            right = random.randint(left, ARRAY_SIZE - 1)
            queries.append(("Range", left, right))
    else:
        query_type = random.choices(["Range", "Update"], weights=[90, 10], k=1)[0]
        if query_type == "Range":
            left = random.randint(0, ARRAY_SIZE - 1)
            right = random.randint(left, ARRAY_SIZE - 1)
            queries.append(("Range", left, right))
        else:  # Update
            index = random.randint(0, ARRAY_SIZE - 1)
            value = random.randint(1, 100)
            queries.append(("Update", index, value))

range_count = sum(1 for query in queries if query[0] == "Range")
update_count = sum(1 for query in queries if query[0] == "Update")

print(f"Кількість Range запитів: {range_count}")
print(f"Кількість Update запитів: {update_count}")
print(f"Відсоток Range запитів: {range_count / QUERY_COUNT * 100:.2f}%")
print(f"Відсоток Update запитів: {update_count / QUERY_COUNT * 100:.2f}%")


# Define functions for timeit
def execute_no_cache():
    for query in queries:
        if query[0] == "Range":
            processor.range_sum_no_cache(query[1], query[2])
        elif query[0] == "Update":
            processor.update_no_cache(query[1], query[2])


def execute_with_cache():
    for query in queries:
        if query[0] == "Range":
            processor.range_sum_with_cache(query[1], query[2])
        elif query[0] == "Update":
            processor.update_with_cache(query[1], query[2])


# Measure execution time using timeit
no_cache_time = timeit.timeit(execute_no_cache, number=1)
cache_time = timeit.timeit(execute_with_cache, number=1)

# Output the results
print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")

processor.print_stats()
