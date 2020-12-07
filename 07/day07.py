from collections import defaultdict
from typing import Tuple, List, Dict
import re


bag_spec_re = re.compile(r'(^\d+) (.*)$')


def cleanup_color(color: str) -> str:
    if color[-1] == '.':
        color = color[:-1]
    if color[-1] == 's':
        color = color[:-1]
    return color


def parse_rule(rule: str) -> Tuple[str, Dict[str, int]]:
    outer, inner_set = rule.split(" contain ")
    outer = cleanup_color(outer)
    inner = {}
    for inner_spec in inner_set.split(", "):
        match = bag_spec_re.match(inner_spec)
        if match:
            inner[cleanup_color(match.group(2))] = int(match.group(1))

    return outer, inner


def close_contents(color: str, contained_by: Dict[str, List[str]]) -> List[str]:
    search_list = contained_by[color]
    already_searched = set()
    results = set()
    while search_list:
        target = search_list.pop()
        if target not in already_searched:
            results.add(target)
            search_list.extend(contained_by[target])
    return results


def count_contained_bags(color: str, contains: Dict[str, Dict[str, int]]) -> int:
    return sum(multiple * (1 + count_contained_bags(inner, contains)) for inner, multiple in contains[color].items())


with open('input.txt', 'r') as f:
    rules = [line.strip() for line in f.readlines()]

contained_by = defaultdict(list)
contains = {}
for rule in rules:
    outer, inner = parse_rule(rule)
    contains[outer] = inner
    for inner_color in inner.keys():
        contained_by[inner_color].append(outer)

sgb = "shiny gold bag"
results = close_contents(sgb, contained_by)
print('Bag colors holding {}s: {}'.format(sgb, len(results)))

print('Bags inside the {}: {}'.format(sgb, count_contained_bags(sgb, contains)))
