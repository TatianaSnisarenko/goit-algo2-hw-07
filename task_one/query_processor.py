from lru_cache import LRUCache


class QueryProcessor:
    def __init__(self, array, capacity=1000):
        self.array = array
        self.cache = LRUCache(capacity)

    def range_sum_no_cache(self, left, right):
        """
        Calculate the sum of elements in the array from index left to right (inclusive).
        This function does not use caching.
        """
        if left < 0 or right >= len(self.array) or left > right:
            raise ValueError("Invalid range")

        return sum(self.array[left : right + 1])

    def update_no_cache(self, index, value):
        """
        Update the value at the specified index in the array.
        This function does not use caching.
        """
        if index < 0 or index >= len(self.array):
            raise ValueError("Index out of range")

        self.array[index] = value

    def range_sum_with_cache(self, left, right):
        """
        Calculate the sum of elements in the array from index left to right (inclusive).
        This function uses caching.
        """
        if left < 0 or right >= len(self.array) or left > right:
            raise ValueError("Invalid range")
        key = (left, right)
        cached = self.cache.get(key)
        if cached != -1:
            return cached
        result = sum(self.array[left : right + 1])
        self.cache.put(key, result)

    def update_with_cache(self, index, value):
        """
        Update the value at the specified index in the array.
        This function uses caching.
        """
        if index < 0 or index >= len(self.array):
            raise ValueError("Index out of range")

        self.array[index] = value
        # Invalidate the cache for all ranges that include the updated index
        self.cache.remove_keys_matching_condition(lambda key: key[0] <= index <= key[1])

    def print_stats(self):
        """
        Print cache statistics in a readable format.
        """
        stats = self.cache.get_stats()
        print(f"Cache Hits: {stats['hits']}")
        print(f"Cache Misses: {stats['misses']}")
        print(f"Cache Hit Rate: {stats['hit_rate']}")
