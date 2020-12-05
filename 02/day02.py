class SledPolicy:
    def __init__(self, definition: str):
        left_right, self.character = definition.split(' ')
        self.minimum, self.maximum = map(int, left_right.split('-'))

    def is_valid_password(self, candidate: str) -> bool:
        count = candidate.count(self.character)
        return self.minimum <= count <= self.maximum


class TobogganPolicy:
    def __init__(self, definition: str):
        left_right, self.character = definition.split(' ')
        self.positions = map(int, left_right.split('-'))

    def is_valid_password(self, candidate: str) -> bool:
        match_count = list(candidate[n-1] for n in self.positions).count(self.character)
        return match_count == 1


def check_password(datum: str, policy_factory) -> bool:
    policy_definition, password = datum.split(':')
    policy = policy_factory(policy_definition)
    return policy.is_valid_password(password.strip())


with open("input.txt", 'r') as file:
    entries = file.readlines()

results = [check_password(entry, SledPolicy) for entry in entries]
print(results.count(True))

results = [check_password(entry, TobogganPolicy) for entry in entries]
print(results.count(True))
