import os.path
import heapq

from aoc_utils.unionfind import UnionFind

DATA = os.path.join(os.path.dirname(__file__), 'day08.txt')

# Part 1 asks us to connect the 1000 closest pairs of junction boxes.
CONNECTIONS_IN_PART_ONE = 1000


def __parse_junction_boxes(data) -> list:
    junction_boxes = []
    for line in data.splitlines():
        coords = line.split(",")
        junction_boxes.append((int(coords[0]), int(coords[1]), int(coords[2])))
    return junction_boxes


def __squared_distance(p, q) -> int:
    # Only ordering matters, so squared distance avoids sqrt and is exact
    # for integer coordinates (no floating-point ties near the 1000th pair).
    return (p[0] - q[0])**2 + (p[1] - q[1])**2 + (p[2] - q[2])**2


def part_one(data, connections=CONNECTIONS_IN_PART_ONE) -> int:
    junction_boxes = __parse_junction_boxes(data)
    distances_pq = []

    for i in range(len(junction_boxes)):
        for j in range(i + 1, len(junction_boxes)):
            heapq.heappush(distances_pq, (__squared_distance(junction_boxes[i], junction_boxes[j]), (i, j)))

    uf = UnionFind()
    remaining = connections

    while remaining != 0:
        _, box = heapq.heappop(distances_pq)
        uf.union(box[0], box[1])
        remaining -= 1

    components = sorted(uf.components(), key=lambda c: len(c), reverse=True)
    return len(components[0]) * len(components[1]) * len(components[2])


def part_two(data) -> int:
    junction_boxes = __parse_junction_boxes(data)
    junction_boxes_len = len(junction_boxes)
    distances_pq = []

    for i in range(len(junction_boxes)):
        for j in range(i + 1, len(junction_boxes)):
            heapq.heappush(distances_pq, (__squared_distance(junction_boxes[i], junction_boxes[j]), (i, j)))

    uf = UnionFind()

    # Optimisation to ensure we're
    # not making expensive calls to
    # `uf.components()` needlessly.
    # We only want to make those
    # calls when we know we've
    # `union`/connected every junction
    # box.
    junction_boxes_connected = set()

    while len(distances_pq) != 0:
        _, box = heapq.heappop(distances_pq)
        uf.union(box[0], box[1])
        junction_boxes_connected.add(box[0])
        junction_boxes_connected.add(box[1])
        if len(junction_boxes_connected) == junction_boxes_len and uf.n_comps == 1:
            return junction_boxes[box[0]][0] * junction_boxes[box[1]][0]

    raise Exception("No solution!")


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
