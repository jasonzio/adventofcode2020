from typing import List
import copy

class Seat:
    def __init__(self, char: str):
        self.occupancy = char

    @staticmethod
    def filled_seat():
        return Seat('#')

    @staticmethod
    def vacant_seat():
        return Seat('L')

    @property
    def occupied(self) -> bool:
        return self.occupancy == '#'

    @property
    def vacant(self) -> bool:
        return self.occupancy == 'L'

    def is_wall(self) -> bool:
        return self.occupancy == 'W'

    def count(self) -> int:
        return 1 if self.occupancy == '#' else 0

    def clone(self):
        return Seat(self.occupancy)


class Room:
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, floor_plan: List[str]):
        self.points = {}        # Dense map of all points in the room
        self.chairs = []        # List of keys in the map where there's a chair

        # Add walls to the room
        width = len(floor_plan[0])
        length = len(floor_plan)
        wall = Seat('W')
        for col_num in range(-1, width+1):
            self.points[(col_num, -1)] = wall
            self.points[(col_num, length)] = wall
        for row_num in range(0, length):
            self.points[(-1, row_num)] = wall
            self.points[(width, row_num)] = wall

        # Populate the points
        for row_num, row in enumerate(floor_plan):
            for col_num, symbol in enumerate(row):
                point = (col_num, row_num)
                self.points[point] = Seat(symbol)
                if symbol != '.':
                    self.chairs.append(point)

    def next_gen(self, rule, density) -> bool:
        new_floor = copy.copy(self.points)
        changed = False
        for x, y in self.chairs:
            count = rule(self, x, y)
            point = (x, y)
            if self.points[point].vacant and count == 0:
                changed = True
                new_floor[point] = Seat.filled_seat()
            elif self.points[point].occupied and count >= density:
                new_floor[point] = Seat.vacant_seat()
                changed = True
            else:
                new_floor[point] = self.points[point].clone()
        self.points = new_floor
        return changed

    def part1_rule(self, x, y):
        return sum(map(Seat.count, [self.points[(x + dx, y + dy)] for dx, dy in Room.deltas]))

    def part2_rule(self, x, y):
        def see_occupied(dx, dy) -> int:
            cx = x + dx
            cy = y + dy
            while not self.points[(cx, cy)].is_wall():
                if self.points[(cx, cy)].occupied:
                    return 1
                elif self.points[(cx, cy)].vacant:
                    return 0
                cx += dx
                cy += dy
            return 0
        return sum(see_occupied(dx, dy) for dx, dy in Room.deltas)

    def count_occupied(self):
        return sum(map(Seat.count, [self.points[point] for point in self.chairs]))


with open('input.txt', 'r') as f:
    layout = [row.strip() for row in f.readlines()]

room = Room(layout)
while room.next_gen(Room.part1_rule, 4):
    print('.', end='')
print("\nPart 1:", room.count_occupied())

room = Room(layout)
while room.next_gen(Room.part2_rule, 5):
    print('.', end='')
print("\nPart 2:", room.count_occupied())

