import os.path

DATA = os.path.join(os.path.dirname(__file__), 'day01.txt')


def part_one(data) -> int:
    result = 0
    dial = 50
    for line in data.splitlines():
        direction, distance = line[0], int(line[1:])
        dial = (dial - distance) % 100 if direction == "L" else (dial + distance) % 100
        if dial == 0:
            result += 1
    return result


def part_two(data) -> int:
    result = 0
    dial = 50
    for line in data.splitlines():
        direction, distance = line[0], int(line[1:])
        prev_dial = dial

        (end, step) = ((dial - distance), -1) if direction == "L" else ((dial + distance), 1)
        dial = end % 100

        for idx in range(prev_dial, end, step):
            if idx % 100 == 0:
                result += 1
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
