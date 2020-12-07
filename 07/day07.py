from collections import defaultdict
from typing import Tuple, List, Dict, Set
import re


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


def close_contents(color: str, contained_by: Dict[str, List[str]]) -> Set[str]:
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
    parsed_rules = [parse_rule(line.strip()) for line in f.readlines()]

contains = {outer: inner for outer, inner in parsed_rules}
contained_by = defaultdict(list)
[contained_by[ic].append(outer) for outer, inner in contains.items() for ic in inner.keys()]

sgb = "shiny gold bag"
print('Bag colors holding a {}: {}'.format(sgb, len(close_contents(sgb, contained_by))))
print('Bags inside the {}: {}'.format(sgb, count_contained_bags(sgb, contains)))
