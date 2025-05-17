from functools import lru_cache
from typing import Any


@lru_cache(maxsize=None)
def fibonacci_lru(n: int) -> int:
    """
    Calculate the nth Fibonacci number using LRU cache for memoization.

    Args:
        n (int): The position of the Fibonacci number to calculate (0-based index).

    Returns:
        int: The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n: int, tree: Any) -> int:
    """
    Calculate the nth Fibonacci number using a Splay Tree for memoization.

    Args:
        n (int): The position of the Fibonacci number to calculate (0-based index).
        tree (Any): An instance of a Splay Tree to store previously calculated Fibonacci numbers.

    Returns:
        int: The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n <= 1:
        return n
    # Check if the result is already in the Splay Tree
    if (result := tree.find(n)) is not None:
        return result
    # Calculate the Fibonacci number recursively
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    # Store the result in the Splay Tree
    tree.insert(n, result)
    return result
