from typing import Tuple

motion = {
    'N': (0, 1),
    'S': (0, -1),
    'E': (1, 0),
    'W': (-1, 0)
}

# 0 is east; turning R90 is S, so 1 char later, turning L90 is N and 1 char earlier
directional = "ESWN"


def decode(move: str) -> Tuple[str, int]:
    return move[0], int(move[1:])


with open('input.txt', 'r') as f:
    instructions = [move.strip() for move in f.readlines()]


def part1(moves) -> int:
    x = 0
    y = 0
    direction = 0
    dx, dy = motion[directional[direction]]

    for move in moves:
        command, arg = decode(move)

        if command in 'NSEW':
            lx, ly = motion[command]
            x += arg * lx
            y += arg * ly
        elif command in 'LR':
            arg = int(arg / 90)
            if command == 'L':
                arg = -arg
            direction = (direction + arg) % 4
            dx, dy = motion[directional[direction]]
        elif command == 'F':
            x += arg * dx
            y += arg * dy
        else:
            raise Exception('Unknown command {}'.format(command))
    return abs(x)+abs(y)


def part2(moves) -> int:
    # x and y are ship's position
    x = 0
    y = 0
    # wx and wy are the location of the waypoint relative to the ship
    wx = 10
    wy = 1

    for move in moves:
        command, arg = decode(move)

        if command in 'NSEW':
            lx, ly = motion[command]
            wx += arg * lx
            wy += arg * ly
        elif command == 'F':    # Move to the waypoint N times
            x += arg * wx
            y += arg * wy
        elif command == 'R':
            for _ in range(int(arg / 90)):
                wx, wy = wy, -wx
        elif command == 'L':
            for _ in range(int(arg / 90)):
                wx, wy = -wy, wx
        else:
            raise Exception('Unknown command {}'.format(command))

    return abs(x) + abs(y)


print('Part 1:', part1(instructions))

test = ['F10', 'N3', 'F7', 'R90', 'F11']
#print('test', part2(test))
print('Part 2:', part2(instructions))
