import os.path

DATA = os.path.join(os.path.dirname(__file__), 'day05.txt')


def __parse_ranges_and_ids(data) -> tuple:
    ranges, ids = [], []
    parsing_ids = False
    for line in data.splitlines():
        if line == "":
            parsing_ids = True
            continue

        if parsing_ids:
            ids.append(int(line))
        else:
            left, right = line.split("-")
            ranges.append((int(left), int(right)))
    return ranges, ids


def part_one(data) -> int:
    result = 0
    ranges, ids = __parse_ranges_and_ids(data)
    for ingredient_id in ids:
        for r in ranges:
            if r[0] <= ingredient_id <= r[1]:
                result += 1
                break
    return result


def part_two(data) -> int:
    result = 0
    ranges, _ = __parse_ranges_and_ids(data)

    # sorting the ranges means we only
    # have to deal with 2 cases:
    # - a range completely within another range
    # - a range overlapping with its left/start number
    ranges.sort()

    for i in range(len(ranges)):
        r1 = ranges[i]
        if r1 is None:
            continue
        for j in range(i + 1, len(ranges)):
            r2 = ranges[j]
            if r2 is None:
                continue
            # entire range is within the other range
            if r1[0] <= r2[0] <= r1[1] and r1[0] <= r2[1] <= r1[1]:
                ranges[j] = None
            # left overlap
            elif r1[0] <= r2[0] <= r1[1] <= r2[1]:
                ranges[j] = (r1[1] + 1,  r2[1])
            else:
            # once we find the first disjoint range
            # all other ranges thereafter will also
            # be disjoint, so we terminate early
                break
        result += (r1[1] - r1[0]) + 1

    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
