import operator
from collections import defaultdict
from functools import lru_cache, reduce
from typing import Tuple, Dict
import re
import datetime as dt


bag_spec_re = re.compile(r'(^\d+) (.*)$')


def parse_rule(rule: str) -> Tuple[str, Dict[str, int]]:
    def normalize_color(color: str) -> str:
        if color[-1] == '.':
            color = color[:-1]
        if color[-1] == 's':
            color = color[:-1]
        return color

    outer, inner_set = rule.split(" contain ")
    outer = normalize_color(outer)
    inner = {}
    for inner_spec in inner_set.split(", "):
        match = bag_spec_re.match(inner_spec)
        if match:
            inner[normalize_color(match.group(2))] = int(match.group(1))

    return outer, inner


@lru_cache(maxsize=None)
def is_x_in_y(target: str, outer: str) -> bool:
    return target in contains[outer] \
           or reduce(operator.or_, [is_x_in_y(target, bag) for bag in contains[outer].keys()], False)


@lru_cache(maxsize=None)
def count_contained_bags(color: str) -> int:
    return sum(multiple * (1 + count_contained_bags(inner)) for inner, multiple in contains[color].items())


time_start = dt.datetime.now()
with open('input.txt', 'r') as f:
    parsed_rules = [parse_rule(line.strip()) for line in f.readlines()]
time_end_io = dt.datetime.now()
contains = {outer: inner for outer, inner in parsed_rules}
contained_by = defaultdict(list)
[contained_by[ic].append(outer) for outer, inner in contains.items() for ic in inner.keys()]
time_end_build = dt.datetime.now()
sgb = "shiny gold bag"
count = sum([1 if is_x_in_y(sgb, bag) else 0 for bag in contains.keys()])
print('Bag colors holding a {}: {}'.format(sgb, count))
time_end_part1 = dt.datetime.now()
print('Bags inside the {}: {}'.format(sgb, count_contained_bags(sgb)))
time_end_part2 = dt.datetime.now()

print("""
IO time: {}
Data structure built: {}
Part 1 only: {}
Part 2 only: {}
All but I/O: {}
Total time: {}
""".format(time_end_io - time_start, time_end_build - time_end_io, time_end_part1 - time_end_io,
           time_end_part2 - time_end_part1, time_end_part2 - time_end_io, time_end_part2 - time_start))
