import os.path

from collections import deque, defaultdict
from shapely.geometry import Polygon, box
from aoc_utils.timer import time_it

DATA = os.path.join(os.path.dirname(__file__), 'day09.txt')


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


def __point_in_polygon(point, polygon_set, bbox, y_index, bucket_size=10) -> bool:
    x, y = point
    minx, miny, maxx, maxy = bbox

    if point in polygon_set:
        return True

    # Fast reject
    if x < minx or x > maxx or y < miny or y > maxy:
        return False

    bucket = int(y // bucket_size)
    edges = y_index.get(bucket, [])

    inside = False
    for x1, y1, x2, y2 in edges:
        if (y1 > y) != (y2 > y):
            x_int = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_int:
                inside = not inside

    return inside


def __discover_outer_region(perimeter_points) -> set:
    visited = set()
    queue = deque()
    perimeter_points_set = set(perimeter_points)

    min_x = min(perimeter_points, key=lambda p: p[0])[0] - 1
    min_y = min(perimeter_points, key=lambda p: p[1])[1] - 1
    max_x = max(perimeter_points, key=lambda p: p[0])[0] + 1
    max_y = max(perimeter_points, key=lambda p: p[1])[1] + 1

    start = (min_x, min_y)

    queue.append(start)
    visited.add(start)

    while len(queue) != 0:
        pos = queue.popleft()

        for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x = pos[0] + d[0]
            new_y = pos[1] + d[1]

            if min_x <= new_x < max_x and min_y <= new_y < max_y and (new_x, new_y) not in visited:
                if (new_x, new_y) not in perimeter_points_set:
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y))
    return visited


def __get_green_tiles_and_perimeter_points(red_tiles) -> tuple:
    perimeter_points = []
    green_tiles = []
    for i in range(len(red_tiles)):
        current = red_tiles[i]
        next_tile = red_tiles[(i + 1) % len(red_tiles)]
        perimeter_points.append(current)
        if current[0] == next_tile[0]:
            start, end = min(current[1], next_tile[1]), max(current[1], next_tile[1])
            for j in range(start + 1, end):
                green_tiles.append((current[0], j))
                perimeter_points.append((current[0], j))
        elif current[1] == next_tile[1]:
            start, end = min(current[0], next_tile[0]), max(current[0], next_tile[0])
            for j in range(start + 1, end):
                green_tiles.append((current[0], j))
                perimeter_points.append((j, current[1]))
        perimeter_points.append(next_tile)

    return green_tiles, perimeter_points


def __rectangle_border_points(min_x, min_y, max_x, max_y):
    border_points = set()

    for y in range(min_y, max_y + 1):
        border_points.add((min_x, y))
        border_points.add((max_x, y))

    for x in range(min_x, max_x + 1):
        border_points.add((x, min_y))
        border_points.add((x, max_y))

    return border_points


def preprocess_polygon(poly) -> tuple:
    edges = []
    minx = miny = float("inf")
    maxx = maxy = float("-inf")

    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]

        minx = min(minx, x1)
        maxx = max(maxx, x1)
        miny = min(miny, y1)
        maxy = max(maxy, y1)

        if y1 != y2:  # ignore horizontal edges
            edges.append((x1, y1, x2, y2))

    return edges, (minx, miny, maxx, maxy)


def build_y_index(edges, bucket_size=10) -> dict:
    index = defaultdict(list)

    for x1, y1, x2, y2 in edges:
        y_min = min(y1, y2)
        y_max = max(y1, y2)

        b_min = int(y_min // bucket_size)
        b_max = int(y_max // bucket_size)

        for b in range(b_min, b_max + 1):
            index[b].append((x1, y1, x2, y2))

    return index


@time_it
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


def part_two_alternate_solution(data) -> int:
    result = -1
    red_tiles = __parse_red_tiles(data)
    _, perimeter_points = __get_green_tiles_and_perimeter_points(red_tiles)
    # __discover_outer_region(perimeter_points)
    perimeter_points_set = set(perimeter_points)

    edges, bbox = preprocess_polygon(perimeter_points)
    y_index = build_y_index(edges, bucket_size=10)

    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            corners = __get_corners(red_tiles[i], red_tiles[j])
            if len(corners) == 2:
                continue
            max_i = max(corners, key=lambda c: c[0])[0]
            max_j = max(corners, key=lambda c: c[1])[1]
            min_i = min(corners, key=lambda c: c[0])[0]
            min_j = min(corners, key=lambda c: c[1])[1]

            all_in_bounds = True
            for cc in corners:
                if not __point_in_polygon(cc, perimeter_points_set, bbox, y_index, bucket_size=10):
                    all_in_bounds = False
                    break

            if not all_in_bounds:
                continue

            rectangle_border_points = __rectangle_border_points(min_i, min_j, max_i, max_j)
            for rp in rectangle_border_points:
                if not __point_in_polygon(rp, perimeter_points_set, bbox, y_index, bucket_size=10):
                    all_in_bounds = False
                    break

            if all_in_bounds:
                result = max(result, __calculate_area(red_tiles[i], red_tiles[j]))

    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
        print("Part 2 (alternate): " + str(part_two_alternate_solution(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
