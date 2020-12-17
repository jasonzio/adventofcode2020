import itertools
from typing import Tuple, List, Set


def neighbors(point: Tuple, offsets: List[Tuple]) -> Set[Tuple]:
    dimensions = len(point)
    all_neighbors = set()
    for offset in offsets:
        if offset != (0,) * dimensions:
            all_neighbors.add(tuple(p + d for p, d in zip(point, offset)))
    return all_neighbors


def compute(initial_state: Set[Tuple], deltas: List[Tuple]) -> Set[Tuple]:
    grid = initial_state.copy()
    for cycle in range(6):
        new_grid = set()
        neighbors_of_all_points = (neighbors(point, deltas) for point in grid)
        points_to_check = set.union(*neighbors_of_all_points)
        points_to_check.update(grid)

        for point in points_to_check:
            count = sum(1 if p in grid else 0 for p in neighbors(point, deltas))
            if point in grid and count in (2, 3):
                new_grid.add(point)
            elif point not in grid and count == 3:
                new_grid.add(point)

        grid = new_grid
    return grid


starting_grid = set()
with open('input.txt', 'r') as f:
    raw_lines = [line.strip() for line in f.readlines()]

for y, line in enumerate(raw_lines):
    for x, c in enumerate(line):
        if c == '#':
            starting_grid.add((x, y, 0))
deltas_3d = list(itertools.product((-1, 0, +1), repeat=3))
result = compute(starting_grid, deltas_3d)
print("part 1:", len(result))

starting_grid.clear()
for y, line in enumerate(raw_lines):
    for x, c in enumerate(line):
        if c == '#':
            starting_grid.add((x, y, 0, 0))
deltas_4d = list(itertools.product((-1, 0, +1), repeat=4))
result = compute(starting_grid, deltas_4d)
print("part 2:", len(result))
