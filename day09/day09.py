import os.path

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


def __build_inside_cells(red_tiles):
    """Mark which compressed grid cells lie inside the polygon.

    The red tiles, joined in order, form a rectilinear polygon. Compressing
    the distinct x and y coordinates gives a grid whose cells are either
    wholly inside or wholly outside the polygon. We find the inside cells with
    an even-odd scanline over the polygon's vertical edges.

    Returns the sorted coordinate lists, coordinate->index maps and the
    ``inside`` matrix (indexed ``[x_cell][y_cell]``).
    """
    xs = sorted({x for x, _ in red_tiles})
    ys = sorted({y for _, y in red_tiles})
    x_index = {x: i for i, x in enumerate(xs)}
    y_index = {y: i for i, y in enumerate(ys)}

    vertical_edges = []
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]
        if x1 == x2:
            vertical_edges.append((x1, min(y1, y2), max(y1, y2)))

    inside = [[False] * (len(ys) - 1) for _ in range(len(xs) - 1)]

    for j in range(len(ys) - 1):
        y_mid = ys[j] + 0.5
        crossings = sorted(x for x, y_lo, y_hi in vertical_edges if y_lo < y_mid < y_hi)
        for k in range(0, len(crossings), 2):
            left = x_index[crossings[k]]
            right = x_index[crossings[k + 1]]
            for i in range(left, right):
                inside[i][j] = True

    return xs, ys, x_index, y_index, inside


def __build_prefix(inside) -> list:
    """2D prefix sums of the inside matrix, so cell-rectangle sums are O(1)."""
    rows = len(inside)
    cols = len(inside[0]) if rows else 0
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for i in range(rows):
        row_sum = 0
        for j in range(cols):
            row_sum += inside[i][j]
            prefix[i + 1][j + 1] = prefix[i][j + 1] + row_sum
    return prefix


def __inside_cell_count(prefix, x_lo, x_hi, y_lo, y_hi) -> int:
    return prefix[x_hi][y_hi] - prefix[x_lo][y_hi] - prefix[x_hi][y_lo] + prefix[x_lo][y_lo]


@time_it
def part_one(data) -> int:
    result = -1
    red_tiles = __parse_red_tiles(data)
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            result = max(result, __calculate_area(red_tiles[i], red_tiles[j]))
    return result


@time_it
def part_two(data) -> int:
    result = -1
    red_tiles = __parse_red_tiles(data)
    _, _, x_index, y_index, inside = __build_inside_cells(red_tiles)
    prefix = __build_prefix(inside)

    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, len(red_tiles)):
            x2, y2 = red_tiles[j]

            # A degenerate "rectangle" is just a line; skip it.
            if x1 == x2 or y1 == y2:
                continue

            x_lo, x_hi = sorted((x_index[x1], x_index[x2]))
            y_lo, y_hi = sorted((y_index[y1], y_index[y2]))

            # The rectangle is valid iff every compressed cell it covers is
            # inside the polygon.
            cells = (x_hi - x_lo) * (y_hi - y_lo)
            if __inside_cell_count(prefix, x_lo, x_hi, y_lo, y_hi) == cells:
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
