import itertools
import functools
import operator
from typing import Tuple, List


def find_solutions(entries: List[int], n: int, target: int) -> List[Tuple]:
    return [combo for combo in itertools.combinations(entries, n) if sum(combo) == target]


with open('input.txt', "r") as data:
    entries = [int(entry.strip()) for entry in data.readlines()]

solutions = find_solutions(entries, 2, 2020)
print(functools.reduce(operator.mul, solutions[0], 1))
solutions = find_solutions(entries, 3, 2020)
print(functools.reduce(operator.mul, solutions[0], 1))
