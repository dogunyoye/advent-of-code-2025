import os.path
from collections import deque

DATA = os.path.join(os.path.dirname(__file__), 'day07.txt')


def __generate_grid(data) -> tuple:
    grid = {}
    start = (-1, -1)
    i = 0
    for line in data.splitlines():
        for j, c in enumerate(line):
            if c == "S":
                start = (i, j)
            grid[(i, j)] = c
        i += 1
    return grid, start


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
    grid, start = __generate_grid(data)
    splitters = {pos for pos, value in grid.items() if value == "^"}
    visited = set()
    queue = deque([start])

    while len(queue) != 0:
        beam = queue.popleft()
        next_beam = (beam[0] + 1, beam[1])

        if next_beam in splitters:
            result += 1
            for split in ((next_beam[0], next_beam[1] - 1), (next_beam[0], next_beam[1] + 1)):
                if split not in visited:
                    visited.add(split)
                    queue.append(split)
        elif next_beam in grid and next_beam not in visited:
            visited.add(next_beam)
            queue.append(next_beam)

    return result


def part_two(data) -> int:
    grid, start = __generate_grid(data)
    return __determine_number_of_timelines(grid, start, {})


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
