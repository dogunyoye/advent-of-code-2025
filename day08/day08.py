import math
import os.path

# pip install pyunionfind
from unionfind import UnionFind

DATA = os.path.join(os.path.dirname(__file__), 'day08.txt')


def __parse_junction_boxes(data) -> list:
    junction_boxes = []
    for line in data.splitlines():
        coords = line.split(",")
        junction_boxes.append((int(coords[0]), int(coords[1]), int(coords[2])))
    return junction_boxes


def __euclidean_distance(p, q) -> float:
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2 + (p[2] - q[2])**2)


def part_one(data) -> int:
    junction_boxes = __parse_junction_boxes(data)
    junction_boxes_len = len(junction_boxes)
    distances = []

    for i in range(len(junction_boxes)):
        for j in range(i + 1, len(junction_boxes)):
            distances.append((i, j, __euclidean_distance(junction_boxes[i], junction_boxes[j])))

    distances = sorted(distances, key=lambda d: d[2])[:junction_boxes_len]
    uf = UnionFind()

    for j in distances:
        uf.union(j[0], j[1])

    components = sorted(uf.components(), key=lambda c: len(c), reverse=True)
    return len(components[0]) * len(components[1]) * len(components[2])


def part_two(data) -> int:
    junction_boxes = __parse_junction_boxes(data)
    junction_boxes_len = len(junction_boxes)
    distances = []

    for i in range(len(junction_boxes)):
        for j in range(i + 1, len(junction_boxes)):
            distances.append((i, j, __euclidean_distance(junction_boxes[i], junction_boxes[j])))

    distances = sorted(distances, key=lambda d: d[2])
    uf = UnionFind()

    # Optimisation to ensure we're
    # not making expensive calls to
    # `uf.components()` needlessly.
    # We only want to make those
    # calls when we know we've
    # `union`/connected every junction
    # box.
    junction_boxes_connected = set()

    for j in distances:
        uf.union(j[0], j[1])
        junction_boxes_connected.add(j[0])
        junction_boxes_connected.add(j[1])
        if len(junction_boxes_connected) == junction_boxes_len and uf.n_comps == 1:
            return junction_boxes[j[0]][0] * junction_boxes[j[1]][0]

    raise Exception("No solution!")


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
