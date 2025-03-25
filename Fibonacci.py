from functools import lru_cache
from timeit import timeit
import matplotlib


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    pass


if __name__ == "__main__":
    for times in range(0, 950 + 1, 50):
        execution_time = round(timeit(lambda: fibonacci_lru(times)), 10)
        print(
            f"LRU Cache: Time taken for {times}th Fibonacci number: {execution_time} seconds"
        )

    # for times in range(0, 950 + 1, 50):
    #     start_time_splay = timeit()
    #     fibonacci_splay()
    #     end_time_splay = timeit() - start_time_lru
    #     print(
    #         f"Splay Tree: Time taken for {times}th Fibonacci number: {end_time_splay} seconds"
    #     )
