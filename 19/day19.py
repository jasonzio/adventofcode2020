import re
from typing import Dict


quote_char = re.compile(r'"([ab])"')
do_part2 = False


def build_regex(ruleset: Dict[int, str], start: int) -> str:
    if do_part2:
        if start == 8:
            return r'(?:{})+'.format(build_regex(ruleset, 42))
        elif start == 11:
            r42 = build_regex(ruleset, 42)
            r31 = build_regex(ruleset, 31)
            return '(?:' + '|'.join([r'{}{{{}}}{}{{{}}}'.format(r42, n, r31, n) for n in range(1, 5)]) + ')'
    rule = ruleset[start]
    match = quote_char.match(rule)
    if match:
        return match.group(1)
    elif '|' in rule:
        pieces = [build_sequence(ruleset, part) for part in rule.strip().split('|')]
        return r'(?:{})'.format('|'.join(pieces))
    else:
        return build_sequence(ruleset, rule)


def build_sequence(ruleset: Dict[int, str], sequence: str) -> str:
    pieces = [build_regex(ruleset, int(rule_number)) for rule_number in sequence.strip().split(' ')]
    return r'(?:{})'.format(''.join(pieces))


lines = open("input.txt").read().splitlines()
blank_index = [index for index, line in enumerate(lines) if not line][0]
rules = {int(rule_number): rest for rule_number, rest in [line.split(': ') for line in lines[0:blank_index]]}

raw_regex = r'^{}$'.format(build_regex(rules, 0))
regex = re.compile(raw_regex)

count = 0
for line in lines[blank_index+1:]:
    if regex.match(line):
        count += 1

print('part1', count)

rules[8] = '42 | 42 8'
rules[11] = '42 31 | 42 11 31'

do_part2 = True
raw_regex = r'^{}$'.format(build_regex(rules, 0))
regex = re.compile(raw_regex)

count = 0
for line in lines[blank_index+1:]:
    if regex.match(line):
        count += 1

print('part2', count)
