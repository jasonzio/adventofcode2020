from typing import List, Set, Dict


def chunk_lines(lines: List[str]):
    """
    Given a stream of lines of interesting data separated by a blank line, generate one block of
    interesting data at a time.
    """
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


def count_chunk(lines: List[str]) -> Dict[str, int]:
    answers = {}
    for line in lines:
        for question in line:
            if question in answers:
                answers[question] += 1
            else:
                answers[question] = 1
    return answers


with open('input.txt', 'r') as f:
    data_set = [line.strip() for line in f.readlines()]

count_sets = list([count_chunk(chunk) for chunk in chunk_lines(data_set)])
count_any = [len(count_set) for count_set in count_sets]
print("Sum of questions answered by any: {}".format(sum(count_any)))

set_lengths = list(len(chunk) for chunk in chunk_lines(data_set))
sum_of_answered_by_all = 0
for count_set, set_length in zip(count_sets, set_lengths):
    answered_by_all = [answer for answer in count_set.keys() if count_set[answer] == set_length]
    sum_of_answered_by_all += len(answered_by_all)

print("Sum of questions answered by all: {}".format(sum_of_answered_by_all))

