
import os.path

from shapely.geometry import Polygon, box

DATA = os.path.join(os.path.dirname(__file__), 'day09.txt')


def __print_grid(green_tiles, red_tiles):
    grid = {}
    for g in green_tiles:
        grid[g] = "X"

    for r in red_tiles:
        grid[r] = "#"

    max_i = max(grid, key=lambda x: x[0])
    max_j = max(grid, key=lambda x: x[1])
    for i in range(max_i[0] + 1):
        line = ""
        for j in range(max_j[1] + 1):
            if (i, j) not in grid:
                line += "."
            else:
                line += grid[(i, j)]
        print(line)


def __parse_red_tiles(data) -> list:
    red_tiles = []
    for line in data.splitlines():
        parts = line.split(",")
        red_tiles.append((int(parts[0]), int(parts[1])))
    return red_tiles


def __calculate_area(a, b) -> int:
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def __get_corners(a, b) -> list:
    # horizontal or vertical line
    if a[0] == b[0] or a[1] == b[1]:
        return [a, b]
    return [a, b, (a[0], b[1]), (b[0], a[1])]


def part_one(data) -> int:
    result = -1
    red_tiles = __parse_red_tiles(data)
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            result = max(result, __calculate_area(red_tiles[i], red_tiles[j]))
    return result


def part_two(data) -> int:
    result = -1
    red_tiles = __parse_red_tiles(data)
    poly = Polygon(red_tiles)

    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            corners = __get_corners(red_tiles[i], red_tiles[j])
            if len(corners) == 2:
                continue
            max_i = max(corners, key=lambda c: c[0])[0]
            max_j = max(corners, key=lambda c: c[1])[1]
            min_i = min(corners, key=lambda c: c[0])[0]
            min_j = min(corners, key=lambda c: c[1])[1]
            rectangle = box(min_i, min_j, max_i, max_j)
            if poly.contains(rectangle):
                result = max(result, __calculate_area(red_tiles[i], red_tiles[j]))

    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
