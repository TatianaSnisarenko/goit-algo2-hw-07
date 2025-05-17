from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key):
        """
        Retrieve an item from the cache. If the item is not found, return -1.
        If the item is found, move it to the end to mark it as recently used.
        """
        if key in self.cache:
            # Move the accessed item to the end to mark it as recently used
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return -1

    def put(self, key, value):
        if key in self.cache:
            # Update the value and move the item to the end
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Remove the least recently used item (first item in OrderedDict)
            self.cache.popitem(last=False)

    def remove_keys_matching_condition(self, condition):
        """
        Remove keys from the cache that satisfy the given condition.
        The condition is a callable that takes a key and returns True or False.
        """
        keys_to_delete = [key for key in self.cache if condition(key)]
        for key in keys_to_delete:
            del self.cache[key]

    def reset_capacity(self, new_capacity):
        """
        Reset the capacity of the cache. Clears the cache if the new capacity is smaller.
        """
        self.capacity = new_capacity
        while len(self.cache) > new_capacity:
            self.cache.popitem(last=False)

    def get_stats(self):
        """
        Return cache statistics: hits, misses, and hit rate.
        """
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2f}%",
        }
