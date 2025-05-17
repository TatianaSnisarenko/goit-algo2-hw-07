from collections import OrderedDict
from typing import Callable, Any, Dict


class LRUCache:
    def __init__(self, capacity: int):
        """
        Initialize the LRUCache with a given capacity.

        Args:
            capacity (int): The maximum number of items the cache can hold.
        """
        self.capacity: int = capacity
        self.cache: OrderedDict[Any, Any] = OrderedDict()
        self.hits: int = 0
        self.misses: int = 0

    def get(self, key: Any) -> Any:
        """
        Retrieve an item from the cache. If the item is not found, return -1.
        If the item is found, move it to the end to mark it as recently used.

        Args:
            key (Any): The key of the item to retrieve.

        Returns:
            Any: The value associated with the key, or -1 if the key is not found.
        """
        if key in self.cache:
            # Move the accessed item to the end to mark it as recently used
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return -1

    def put(self, key: Any, value: Any) -> None:
        """
        Add an item to the cache. If the key already exists, update its value
        and mark it as recently used. If the cache exceeds its capacity,
        remove the least recently used item.

        Args:
            key (Any): The key of the item to add or update.
            value (Any): The value to associate with the key.
        """
        if key in self.cache:
            # Update the value and move the item to the end
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Remove the least recently used item (first item in OrderedDict)
            self.cache.popitem(last=False)

    def remove_keys_matching_condition(self, condition: Callable[[Any], bool]) -> None:
        """
        Remove keys from the cache that satisfy the given condition.

        Args:
            condition (Callable[[Any], bool]): A callable that takes a key
            and returns True if the key should be removed, False otherwise.
        """
        keys_to_delete = [key for key in self.cache if condition(key)]
        for key in keys_to_delete:
            del self.cache[key]

    def reset_capacity(self, new_capacity: int) -> None:
        """
        Reset the capacity of the cache. If the new capacity is smaller than
        the current number of items, remove the least recently used items
        until the cache size is within the new capacity.

        Args:
            new_capacity (int): The new maximum capacity of the cache.
        """
        self.capacity = new_capacity
        while len(self.cache) > new_capacity:
            self.cache.popitem(last=False)

    def get_stats(self) -> Dict[str, Any]:
        """
        Return cache statistics, including the number of hits, misses,
        and the hit rate.

        Returns:
            Dict[str, Any]: A dictionary containing the following keys:
                - "hits": The number of cache hits.
                - "misses": The number of cache misses.
                - "hit_rate": The hit rate as a percentage.
        """
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2f}%",
        }
