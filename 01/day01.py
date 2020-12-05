import itertools
import functools
import operator
from typing import Tuple, List


def find_solutions(file: str, n: int, target: int) -> List[Tuple]:
    with open(file, "r") as data:
        raw_entries = data.readlines()

    entries = [int(entry.strip()) for entry in raw_entries]

    solutions = [combo for combo in itertools.combinations(entries, n) if sum(combo) == target]

    return solutions


solutions = find_solutions("input.txt", 2, 2020)
print(functools.reduce(operator.mul, solutions[0], 1))
solutions = find_solutions("input.txt", 3, 2020)
print(functools.reduce(operator.mul, solutions[0], 1))
