import itertools
from typing import Tuple
import operator

def bsp_to_int(spec: str, maximum: int, notation: str) -> int:
    minimum = 0
    for c in spec:
        stride = int((maximum - minimum) / 2)
        if c == notation[0]:    # lower half
            maximum -= stride
        else:
            minimum += stride
    return minimum


def boarding_pass_id(boarding_pass: str) -> int:
    row = bsp_to_int(boarding_pass[:-3], 128, 'FB')
    seat = bsp_to_int(boarding_pass[-3:], 8, 'LR')
    seat_id = row*8 + seat
    return seat_id


with open('input.txt', 'r') as f:
    passes = [bp.strip() for bp in f.readlines()]

seat_ids = [boarding_pass_id(bp) for bp in passes]
seat_ids.sort()
print("Max id: {}".format(seat_ids[-1]))

gaps = map(lambda x: x == 2, map(operator.sub, seat_ids[1:], seat_ids))
missing_seat = next(itertools.compress(seat_ids, gaps)) + 1
print("Your seat is {}".format(missing_seat))





