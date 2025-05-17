import timeit
import matplotlib.pyplot as plt

import pandas as pd
from splay_tree import SplayTree

from fibonacci import fibonacci_lru, fibonacci_splay


fib_numbers = list(range(0, 951, 50))

lru_times = []
splay_times = []

for n in fib_numbers:
    # LRU Cache
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10) * 1000 / 10
    lru_times.append(lru_time)

    # Splay Tree
    splay_tree = SplayTree()
    splay_time = (
        timeit.timeit(lambda: fibonacci_splay(n, splay_tree), number=10) * 1000 / 10
    )
    splay_times.append(splay_time)

# Побудова графіка
plt.plot(fib_numbers, lru_times, label="LRU Cache", marker="o")
plt.plot(fib_numbers, splay_times, label="Splay Tree", marker="o")
plt.xlabel("Число Фібоначчі (n))")
plt.ylabel("Середній час виконання (мс)")
plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
plt.legend()
plt.grid()
plt.show()


data = {
    "n": fib_numbers,
    "LRU Cache Time (ms)": [time for time in lru_times],
    "Splay Tree Time (ms)": [time for time in splay_times],
}
df = pd.DataFrame(data)
print(df)
