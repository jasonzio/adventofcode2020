from typing import List


def part1(starter: List[int], limit) -> int:
    ultimate = {}
    penultimate = {}
    for index, number in enumerate(starter):
        ultimate[number] = index + 1
    last_spoken = starter[-1]
    was_new = True
    for turn in range(len(starter)+1, limit + 1):
        if was_new:
            next_number = 0
        else:
            next_number = ultimate[last_spoken] - penultimate[last_spoken]
        if next_number not in ultimate:
            was_new = True
        else:
            was_new = False
            penultimate[next_number] = ultimate[next_number]
        ultimate[next_number] = turn
        last_spoken = next_number
    return last_spoken


test0 = [0, 3, 6]
#print(part1(test0, 10))

test_cases = [ [1, 3, 2], [2, 1, 3], [1, 2, 3], [2, 3, 1], [3, 2, 1], [3, 1, 2]]
#for case in test_cases:
    #print(case, part1(case, 2020))

part1_starter = [7, 12, 1, 0, 16, 2]
print('Part 1:', part1(part1_starter, 2020))
print('Part 2:', part1(part1_starter, 30000000))