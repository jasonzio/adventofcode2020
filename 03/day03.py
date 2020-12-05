from typing import List
import functools
import operator


def is_collision(position: int, terrain_row: str) -> bool:
    position = position % len(terrain_row)
    collision = terrain_row[position % len(terrain_row)] == '#'
    return collision


def count_collisions(terrain: List[str], rule_across: int, rule_down: int) -> int:
    relevant_terrain = (terrain[n] for n in range(0, len(terrain), rule_down))
    positions = range(0, len(terrain)*rule_across, rule_across)
    collisions = list(map(is_collision, positions, relevant_terrain))
    return collisions.count(True)


with open('input.txt', 'r') as f:
    terrain_set = list(line.strip() for line in f.readlines())

print("Collisions for (3,1) slope: {}".format(count_collisions(terrain_set, 3, 1)))

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
collision_counts = [count_collisions(terrain_set, right, down) for right, down in slopes]
print("Product of collision counts for all slopes: {}".format(functools.reduce(operator.mul, collision_counts, 1)))
