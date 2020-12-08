from typing import List
import re


class Instruction:
    instruction_re = re.compile(r'^([a-z]{3}) ([+-])(\d+)$')

    def __init__(self, text: str):
        match = self.instruction_re.match(text.strip())
        if match:
            self._opcode = match.group(1)
            self._sign = match.group(2)
            self._val = int(match.group(3))
        else:
            raise Exception('Invalid program statement [{}]'.format(text))

    def decode(self):
        return self._opcode, self._sign, self._val

    @property
    def opcode(self):
        return self._opcode

    def dupe_alter_opcode(self, new_op: str):
        """
        Create a new Instruction which differs from self only in the opcode.

        :param new_op: The new opcode
        :rtype: Instruction
        """
        return Instruction("{} {}{}".format(new_op, self._sign, self._val))


class Cpu:
    memory: List[Instruction]

    def __init__(self):
        self.acc = 0
        self.memory = []
        self.dirty = set()
        self.ip = 0

    def get_acc(self) -> int:
        return self.acc

    def load_program(self, program: List[Instruction]):
        self.memory = program

    def run_program(self, start: int) -> str:
        self.acc = 0
        self.dirty = set()
        self.ip = start

        while True:
            if self.ip in self.dirty:
                return "loop"
            elif self.ip == len(self.memory):
                return "exit"
            opcode, sign, val = self.memory[self.ip].decode()
            self.dirty.add(self.ip)
            (Cpu.__dict__[opcode])(self, sign, val)

    def nop(self, *_):
        self.ip += 1

    def acc(self, sign: str, val: int):
        self.acc += -val if sign == "-" else val
        self.ip += 1

    def jmp(self, sign: str, val: int):
        self.ip += -val if sign == "-" else val


def try_mod(program: List[Instruction], ip: int, new_op: str):
    saved_instruction = program[ip]
    program[ip] = saved_instruction.dupe_alter_opcode(new_op)
    test_core = Cpu()
    test_core.load_program(program)
    if test_core.run_program(0) == 'exit':
        print('Part 2: Accumulator is {}'.format(test_core.get_acc()))
        exit(0)
    program[ip] = saved_instruction


with open('input.txt', 'r') as f:
    test_program = [Instruction(line) for line in f.readlines()]

core = Cpu()
core.load_program(test_program)
core.run_program(0)
print("Part 1: Accumulator is {}".format(core.get_acc()))

for address, instruction in enumerate(test_program):
    if instruction.opcode == 'nop':
        try_mod(test_program, address, 'jmp')
    elif instruction.opcode == 'jmp':
        try_mod(test_program, address, 'nop')

print("Part 2: No successful modification found")
