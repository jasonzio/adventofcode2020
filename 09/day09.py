import itertools

with open('input.txt', 'r') as f:
    dataset = [int(x.strip()) for x in f.readlines()]

goal = -1
for end in range(25, len(dataset)):
    goal = dataset[end]
    matches = [pair for pair in itertools.combinations(dataset[end-25:end], 2) if sum(pair) == goal]
    if not matches:
        print("Part 1:", goal)
        break

for begin in range(0, len(dataset)):
    end = begin + 1
    while sum(dataset[begin:end]) < goal and end <= len(dataset):
        end += 1
    if end <= len(dataset) and sum(dataset[begin:end]) == goal:
        winner = dataset[begin:end]
        print("Part 2:", min(winner)+max(winner))
        break
