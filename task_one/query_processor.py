from lru_cache import LRUCache
from typing import List, Tuple


class QueryProcessor:
    def __init__(self, array: List[int], capacity: int = 1000):
        """
        Initialize the QueryProcessor with an array and a cache.

        Args:
            array (List[int]): The array of integers to process.
            capacity (int): The maximum capacity of the LRU cache. Default is 1000.
        """
        self.array = array
        self.cache = LRUCache(capacity)

    def range_sum_no_cache(self, left: int, right: int) -> int:
        """
        Calculate the sum of elements in the array from index `left` to `right` (inclusive).
        This function does not use caching.

        Args:
            left (int): The starting index of the range.
            right (int): The ending index of the range.

        Returns:
            int: The sum of the elements in the specified range.

        Raises:
            ValueError: If the range is invalid (e.g., `left` > `right` or indices are out of bounds).
        """
        if left < 0 or right >= len(self.array) or left > right:
            raise ValueError("Invalid range")

        return sum(self.array[left : right + 1])

    def update_no_cache(self, index: int, value: int) -> None:
        """
        Update the value at the specified index in the array.
        This function does not use caching.

        Args:
            index (int): The index to update.
            value (int): The new value to set at the specified index.

        Raises:
            ValueError: If the index is out of bounds.
        """
        if index < 0 or index >= len(self.array):
            raise ValueError("Index out of range")

        self.array[index] = value

    def range_sum_with_cache(self, left: int, right: int) -> int:
        """
        Calculate the sum of elements in the array from index `left` to `right` (inclusive).
        This function uses caching.

        Args:
            left (int): The starting index of the range.
            right (int): The ending index of the range.

        Returns:
            int: The sum of the elements in the specified range.

        Raises:
            ValueError: If the range is invalid (e.g., `left` > `right` or indices are out of bounds).
        """
        if left < 0 or right >= len(self.array) or left > right:
            raise ValueError("Invalid range")
        key: Tuple[int, int] = (left, right)
        cached = self.cache.get(key)
        if cached != -1:
            return cached
        result = sum(self.array[left : right + 1])
        self.cache.put(key, result)
        return result

    def update_with_cache(self, index: int, value: int) -> None:
        """
        Update the value at the specified index in the array.
        This function uses caching and invalidates affected cache entries.

        Args:
            index (int): The index to update.
            value (int): The new value to set at the specified index.

        Raises:
            ValueError: If the index is out of bounds.
        """
        if index < 0 or index >= len(self.array):
            raise ValueError("Index out of range")

        self.array[index] = value
        # Invalidate the cache for all ranges that include the updated index
        self.cache.remove_keys_matching_condition(lambda key: key[0] <= index <= key[1])

    def print_stats(self) -> None:
        """
        Print cache statistics in a readable format.

        Outputs:
            Cache hits, misses, and hit rate as a percentage.
        """
        stats = self.cache.get_stats()
        print(f"Cache Hits: {stats['hits']}")
        print(f"Cache Misses: {stats['misses']}")
        print(f"Cache Hit Rate: {stats['hit_rate']}")
