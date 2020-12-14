from collections import defaultdict
from typing import Tuple, List
import re


def mask_to_masks(mask: str) -> Tuple[int, int]:
    and_mask = 0
    or_mask = 0
    bits = [c for c in mask]
    bits.reverse()
    for power, c in enumerate(bits):
        if c == '1':
            or_mask += 1 << power
        elif c == '0':
            and_mask += 1 << power
    and_mask = ~(and_mask + (1 << 36))
    return or_mask, and_mask


with open('input.txt', 'r') as f:
    program = [line.strip() for line in f.readlines()]


def run_program(program: List[str]) -> defaultdict:
    memory = defaultdict(int)
    a = 1 << 36 - 1
    o = 0
    decoder = re.compile(r'^mem\[(\d+)] = (\d+)$')
    for stmt in program:
        if stmt.startswith('mask'):
            o, a = mask_to_masks(stmt[7:])
            # print('masks', a, o)
        else:
            parts = decoder.match(stmt)
            addr = int(parts.group(1))
            value = int(parts.group(2))
            value |= o
            value &= a
            memory[addr] = value
    return memory


memory = run_program(program)
print('Part 1:', sum(memory.values()))


class Mask:
    def __init__(self, mask: str):
        bits = [c for c in mask]
        bits.reverse()
        self.or_mask = 0
        self.and_mask = 0
        self.floating = []
        for power, c in enumerate(bits):
            if c == '1':
                self.or_mask += 1 << power
            elif c == 'X':
                self.floating.append(power)
                self.and_mask += 1 << power
        self.and_mask = ~self.and_mask

    def apply(self, address: int):
        base = (address & self.and_mask) | self.or_mask
        if not self.floating:
            return base
        for bitset in range(1 << len(self.floating)):
            value = base
            for whichbit, bitnum in enumerate(self.floating):
                if bitset & (1 << whichbit):
                    value |= (1 << bitnum)
            yield value


def run_program2(program: List[str]) -> defaultdict:
    memory = defaultdict(int)
    decoder = re.compile(r'^mem\[(\d+)] = (\d+)$')
    for stmt in program:
        if stmt.startswith('mask'):
            mask = Mask(stmt[7:])
        else:
            parts = decoder.match(stmt)
            value = int(parts.group(2))
            for address in mask.apply(int(parts.group(1))):
                memory[address] = value
    return memory


memory = run_program2(program)
print('Part 2:', sum(memory.values()))
