import re
from typing import Dict


class Field:
    decode = re.compile(r'^([^:]+): (\d+)-(\d+) or (\d+)-(\d+)$')

    def __init__(self, rule: str):
        matches = Field.decode.match(rule)
        self.name = matches.group(1)
        self.lower1 = int(matches.group(2))
        self.upper1 = int(matches.group(3))
        self.lower2 = int(matches.group(4))
        self.upper2 = int(matches.group(5))

    def is_valid(self, value: str):
        value = int(value)
        return self.lower1 <= value <= self.upper1 or self.lower2 <= value <= self.upper2


def next_line():
    with open('input.txt', 'r') as f:
        for input_line in f.readlines():
            yield input_line.strip()


def validate_field(f_set: Dict[str, Field], v: str) -> bool:
    return len(list(filter(None, [f.is_valid(v) for f in f_set.values()]))) > 0


fields = {}
reader = next_line()
while True:
    line = next(reader)
    if not line:
        break
    field = Field(line)
    fields[field.name] = field

next(reader)     # Skip "your ticket:" header
my_ticket = next(reader)
next(reader)     # skip blank line
next(reader)     # skip "nearby tickets:" header

nearby_tickets = [line for line in reader]

scan_error_rate = 0
valid_tickets = []
for ticket in nearby_tickets:
    is_valid = True
    for value in ticket.split(','):
        if not validate_field(fields, value):
            scan_error_rate += int(value)
            is_valid = False
    if is_valid:
        valid_tickets.append(ticket)

print('part 1', scan_error_rate)

impossible = [set() for i in range(len(my_ticket.split(',')))]

print(valid_tickets)
for ticket in valid_tickets:
    for index, value in enumerate(ticket.split(',')):
        for field in fields.values():
            if not field.is_valid(value) and field.name not in impossible[index]:
                impossible[index].add(field.name)

all_field_names = set(fields.keys())
possible = [all_field_names - impossibilities for impossibilities in impossible]

definitions = {}

while True:
    change = False
    for index, p in enumerate(possible):
        if len(p) == 1:
            name = p.pop()
            definitions[index] = name
            change = True
            for x in possible:
                x.discard(name)
            break
    if not change:
        break

product = 1
my_ticket = [int(x) for x in my_ticket.split(',')]
for index, name in definitions.items():
    if name.startswith('departure'):
        product *= my_ticket[index]

print('Part 2', product)
