import random


def sorter(*args, **kwargs):
    array = [random.randint(0, 100) for _ in range(1000000)]
    array.sort()
