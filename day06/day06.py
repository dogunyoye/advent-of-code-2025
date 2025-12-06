import os.path
from math import prod

DATA = os.path.join(os.path.dirname(__file__), 'day06.txt')


def __print_grid(grid):
    for row in grid:
        for element in row:
            print(element, end=" ")
        print()


def __generate_grid(data) -> list:
    grid = []
    for line in data.splitlines():
        row = line.split()
        grid.append(row)
    return grid


def part_one(data) -> int:
    result = 0
    grid = __generate_grid(data)
    length, depth = len(grid[0]), len(grid)

    for i in range(length):
        nums = []
        for j in range(depth-1):
            nums.append(int(grid[j][i]))
        if grid[depth-1][i] == "*":
            result += prod(nums)
        else:
            result += sum(nums)
    return result


def part_two(data) -> int:
    result = 0
    i, j = 0, 0
    longest_line = -1
    lines = data.splitlines()
    operations = lines[len(lines)-1].split()
    op_idx = 0

    for idx in range(len(lines) - 1):
        longest_line = max(longest_line, len(lines[idx]))

    nums = None
    current_value = ""

    while True:
        if i == 0:
            if nums is None:
                nums = []
            else:
                if current_value == "":
                    if operations[op_idx] == "*":
                        result += prod(nums)
                    else:
                        result += sum(nums)
                    nums = []
                    op_idx += 1
                else:
                    nums.append(int(current_value))
                current_value = ""
                j += 1

        if j >= longest_line:
            if operations[op_idx] == "*":
                return result + prod(nums)
            return result + sum(nums)

        if j <= len(lines[i]) - 1 and lines[i][j] != " ":
            current_value += lines[i][j]

        i = (i + 1) % (len(lines) - 1)


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
