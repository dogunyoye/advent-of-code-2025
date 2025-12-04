import os.path

DATA = os.path.join(os.path.dirname(__file__), 'day04.txt')


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


def __can_access(pos, grid) -> bool:
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx, dy) == (0, 0):
                continue
            neighbor = (pos[0] + dx, pos[1] + dy)
            if neighbor in grid and grid[neighbor] == "@":
                count += 1
    return count < 4


def part_one(data) -> int:
    result = 0
    grid = __generate_grid(data)

    for (k, v) in grid.items():
        if v == "@" and __can_access(k, grid):
            result += 1
    return result


def part_two(data) -> int:
    result = 0
    grid = __generate_grid(data)

    while True:
        removed = []
        count = 0
        for (k, v) in grid.items():
            if v == "@" and __can_access(k, grid):
                count += 1
                removed.append(k)
        if count == 0:
            break
        result += count
        for p in removed:
            grid[p] = '.'
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
