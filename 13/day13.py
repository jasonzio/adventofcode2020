import sys
import copy
from time import sleep

with open('input.txt', 'r') as f:
    test_data = f.readlines()

timestamp = int(test_data[0].strip())
bus_data = test_data[1].strip()
bus_numbers = [int(x) for x in bus_data.split(',') if x != 'x']
wait_times = list(map(lambda t: (t - (timestamp % t)) % t, bus_numbers))
best = timestamp
best_id = 0
for n, wait_time in enumerate(wait_times):
    if wait_time < best:
        best = wait_time
        best_id = n

print("part 1:", bus_numbers[best_id] * best)

bus_delta = {}
for delta, bus_id in enumerate(bus_data.split(',')):
    if bus_id != 'x':
        bus_delta[int(bus_id)] = delta

print(bus_delta)

base = 1
multiple = 1
for bus_id, offset in bus_delta.items():
    print('bus_id', bus_id, 'offset', offset, 'base', base, 'multiple', multiple)
    while (base + offset) % bus_id != 0:
        base += multiple
    multiple *= bus_id

print("Part 2:", base)
