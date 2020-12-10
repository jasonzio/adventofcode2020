from functools import lru_cache, reduce
from itertools import starmap
import operator

with open('input.txt', 'r') as f:
    adaptors = [int(x.strip()) for x in f.readlines()]

adaptors.append(0)
adaptors.sort()
goal = adaptors[-1]+3
adaptors.append(goal)
deltas = list(starmap(operator.sub, zip(adaptors[1:], adaptors[:-1])))
ones = sum(delta for delta in deltas if delta == 1)
threes = int(sum(delta for delta in deltas if delta == 3) / 3)
print('Part 1:', ones*threes)


@lru_cache(None)
def valid(index: int) -> int:
    if index == len(adaptors)-1:
        return 1
    begin = index + 1
    end = min(begin + 3, len(adaptors))
    return reduce(operator.add, [valid(idx) for idx in range(begin, end) if adaptors[idx] - adaptors[index] < 4], 0)


print('Part 2:', valid(0))
