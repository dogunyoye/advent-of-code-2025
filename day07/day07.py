import os.path
from collections import deque

DATA = os.path.join(os.path.dirname(__file__), 'day07.txt')

def __print_grid(grid):
    max_i = max(grid, key=lambda x: x[0])
    max_j = max(grid, key=lambda x: x[1])
    for i in range(max_i[0] + 1):
        line = ""
        for j in range(max_j[1] + 1):
            line += grid[(i, j)]
        print(line)


def __generate_grid(data) -> dict:
    grid = {}
    i = 0
    for line in data.splitlines():
        for j, c in enumerate(line):
            grid[(i, j)] = c
        i += 1
    return grid


def __determine_number_of_timelines(grid, beam, memo) -> int:
    next_beam = (beam[0] + 1, beam[1])
    if next_beam not in grid:
        return 1

    if next_beam in memo:
        return memo[next_beam]

    result = 0
    if grid[next_beam] == ".":
        return __determine_number_of_timelines(grid, next_beam, memo)
    elif grid[next_beam] == "^":
        result += __determine_number_of_timelines(grid, (next_beam[0], next_beam[1] - 1), memo)
        result += __determine_number_of_timelines(grid, (next_beam[0], next_beam[1] + 1), memo)

    memo[beam] = result
    return result


def part_one(data) -> int:
    result = 0
    grid = __generate_grid(data)
    queue = deque()

    for k, v in grid.items():
        if v == "S":
            queue.append(k)
            break

    while len(queue) != 0:
        beam = queue.popleft()
        next_beam = (beam[0] + 1, beam[1])
        if next_beam in grid:
            v = grid[next_beam]
            if v == ".":
                grid[next_beam] = "|"
                queue.append(next_beam)
            elif v == "^":
                split_left = (next_beam[0], next_beam[1] - 1)
                split_right = (next_beam[0], next_beam[1] + 1)
                grid[split_left] = "|"
                grid[split_right] = "|"
                queue.append(split_left)
                queue.append(split_right)
                result += 1

    return result


def part_two(data) -> int:
    grid = __generate_grid(data)
    start = (-1, -1)

    for k, v in grid.items():
        if v == "S":
            start = k
            break

    return __determine_number_of_timelines(grid, start, {})


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
