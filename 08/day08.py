from typing import List, Tuple, Set
import re


class Instruction:
    instruction_re = re.compile(r'^([a-z]{3}) ([+-]?\d+)$')

    def __init__(self, text: str):
        match = self.instruction_re.match(text.strip())
        if match:
            self._opcode = match.group(1)
            self._val = int(match.group(2))
        else:
            raise Exception('Invalid program statement [{}]'.format(text))

    def decode(self) -> Tuple[str, int]:
        return self._opcode, self._val

    @property
    def opcode(self):
        return self._opcode

    def dupe_alter_opcode(self, new_op: str):
        return Instruction("{} {}".format(new_op, self._val))


class Cpu:
    memory: List[Instruction]

    def __init__(self):
        self.acc = 0
        self.memory = []
        self.dirty = set()
        self.ip = 0

    def load_program(self, program: List[Instruction]):
        self.memory = program

    def run_program(self, start: int, break_at: int = -1) -> str:
        while True:
            if self.ip == break_at:
                return "break"
            elif self.ip in self.dirty:
                return "loop"
            elif self.ip == len(self.memory):
                return "exit"
            opcode, val = self.memory[self.ip].decode()
            self.dirty.add(self.ip)
            (Cpu.__dict__[opcode])(self, val)

    def nop(self, *_):
        self.ip += 1

    def acc(self, val: int):
        self.acc += val
        self.ip += 1

    def jmp(self, val: int):
        self.ip += val


def try_mod(program: List[Instruction], tainted: Set[int], ip: int, new_op: str):
    saved_instruction = program[ip]
    program[ip] = saved_instruction.dupe_alter_opcode(new_op)
    test_core = Cpu()
    test_core.load_program(program)
    test_core.run_program(0, break_at=ip)
    test_core.dirty = set(tainted)
    test_core.dirty.discard(ip)
    if test_core.run_program(ip) == 'exit':
        print('Part 2: Fixed instruction at {}. Accumulator is {}'.format(ip, test_core.acc))
        exit(0)
    program[ip] = saved_instruction


with open('input.txt', 'r') as f:
    test_program = [Instruction(line) for line in f.readlines()]

core = Cpu()
core.load_program(test_program)
core.run_program(0)
print("Part 1: Accumulator is {}".format(core.acc))

for address, instruction in enumerate(test_program):
    if instruction.opcode == 'nop':
        try_mod(test_program, core.dirty, address, 'jmp')
    elif instruction.opcode == 'jmp':
        try_mod(test_program, core.dirty, address, 'nop')

print("Part 2: No successful modification found")
