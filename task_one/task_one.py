import random
import timeit
from query_processor import QueryProcessor

# Constants
ARRAY_SIZE: int = 100_000
QUERY_COUNT: int = 50_000
CACHE_SIZE: int = 1000

# Initialize the array and cache
array: list[int] = [random.randint(1, 100) for _ in range(ARRAY_SIZE)]
processor: QueryProcessor = QueryProcessor(array, CACHE_SIZE)

# Generate queries
queries: list[tuple[str, int, int]] = []
for _ in range(QUERY_COUNT):
    if random.random() < 0.9:
        if queries:
            # Reuse a previous query
            queries.append(queries[random.randint(0, len(queries) - 1)])
        else:
            # Generate a new Range query
            left: int = random.randint(0, ARRAY_SIZE - 1)
            right: int = random.randint(left, ARRAY_SIZE - 1)
            queries.append(("Range", left, right))
    else:
        # Generate a new query (Range or Update)
        query_type: str = random.choices(["Range", "Update"], weights=[90, 10], k=1)[0]
        if query_type == "Range":
            left: int = random.randint(0, ARRAY_SIZE - 1)
            right: int = random.randint(left, ARRAY_SIZE - 1)
            queries.append(("Range", left, right))
        else:  # Update
            index: int = random.randint(0, ARRAY_SIZE - 1)
            value: int = random.randint(1, 100)
            queries.append(("Update", index, value))

# Count query types
range_count: int = sum(1 for query in queries if query[0] == "Range")
update_count: int = sum(1 for query in queries if query[0] == "Update")

# Output query statistics
print(f"Number of Range queries: {range_count}")
print(f"Number of Update queries: {update_count}")
print(f"Percentage of Range queries: {range_count / QUERY_COUNT * 100:.2f}%")
print(f"Percentage of Update queries: {update_count / QUERY_COUNT * 100:.2f}%")


def execute_no_cache() -> None:
    """
    Execute all queries without using a cache.

    Iterates through the list of queries and processes each one
    using the non-cached methods of the QueryProcessor.

    Raises:
        Any exceptions raised by the QueryProcessor methods.
    """
    for query in queries:
        if query[0] == "Range":
            processor.range_sum_no_cache(query[1], query[2])
        elif query[0] == "Update":
            processor.update_no_cache(query[1], query[2])


def execute_with_cache() -> None:
    """
    Execute all queries using a cache.

    Iterates through the list of queries and processes each one
    using the cached methods of the QueryProcessor.

    Raises:
        Any exceptions raised by the QueryProcessor methods.
    """
    for query in queries:
        if query[0] == "Range":
            processor.range_sum_with_cache(query[1], query[2])
        elif query[0] == "Update":
            processor.update_with_cache(query[1], query[2])


# Measure execution time using timeit
no_cache_time: float = timeit.timeit(execute_no_cache, number=1)
cache_time: float = timeit.timeit(execute_with_cache, number=1)

# Output the results
print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")

# Print cache statistics
processor.print_stats()
