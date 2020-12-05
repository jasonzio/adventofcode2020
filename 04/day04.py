from typing import List, Generator


class Passport:
    validator = {
        'ecl': lambda x: x in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
        'pid': lambda x: Passport.is_digits(x) and len(x) == 9,
        'eyr': lambda x: Passport.is_number_in_range(x, 2020, 2030),
        'hcl': lambda x: x.startswith('#') and len(x) == 7 and Passport.is_hex_digits(x[1:]),
        'byr': lambda x: Passport.is_number_in_range(x, 1920, 2002),
        'iyr': lambda x: Passport.is_number_in_range(x, 2010, 2020),
        'hgt': lambda x: Passport.is_valid_height(x)
    }

    def __init__(self, dataset: List[str]):
        self.fields = {}
        for line in dataset:
            self.ingest_line(line)

    @staticmethod
    def is_all_charset(text: str, charset: str) -> bool:
        incorrect = [c for c in text if c not in charset]
        return len(incorrect) == 0

    @staticmethod
    def is_digits(text: str) -> bool:
        return Passport.is_all_charset(text, '0123456789')

    @staticmethod
    def is_number_in_range(text: str, minimum: int, maximum: int) -> bool:
        return Passport.is_digits(text) and minimum <= int(text) <= maximum

    @staticmethod
    def is_hex_digits(text: str) -> bool:
        return Passport.is_all_charset(text, '0123456789abcdef')

    @staticmethod
    def is_valid_height(text: str) -> bool:
        if len(text) < 4:
            return False
        units = text[-2:]
        metric = text[:-2]
        metric = int(metric) if Passport.is_digits(metric) else 0
        return (units == 'cm' and 150 <= metric <= 193) or (units == 'in' and 59 <= metric <= 76)

    def is_valid(self) -> bool:
        validations = map(lambda key: key in Passport.validator and Passport.validator[key](self.fields[key]),
                      self.fields.keys())
        return list(validations).count(True) == 7

    def ingest_line(self, line: str):
        for key_value_pair in line.split(' '):
            key, value = key_value_pair.split(':')
            if key != 'cid':
                self.fields[key.strip()] = value.strip()


def chunk_lines(lines: List[str]):
    chunk = []
    for line in lines:
        line = line.strip()
        if not line:
            yield chunk
            chunk = []
        else:
            chunk.append(line)
    if len(chunk):
        yield chunk


with open('input.txt', 'r') as f:
    data = [line.strip() for line in f.readlines()]

results = [Passport(chunk).is_valid() for chunk in chunk_lines(data)]
print(results.count(True))
