import os.path

DATA = os.path.join(os.path.dirname(__file__), 'day02.txt')


def chunks_valid(chunk: list, c_str: str) -> bool:
    length = 0
    for c in chunk:
        length += len(c)
    return length == len(c_str)


def part_one(data) -> int:
    result = 0
    ranges = data.splitlines()[0].strip().split(",")
    for r in ranges:
        id_range = r.split("-")
        start, end = int(id_range[0]), int(id_range[1])
        for c in range(start, end+1):
            c_str = str(c)
            if len(c_str) % 2 == 0 and c_str[0:len(c_str)//2] == c_str[len(c_str)//2:]:
                result += c
    return result


def part_two(data) -> int:
    result = 0
    ranges = data.splitlines()[0].strip().split(",")
    for r in ranges:
        id_range = r.split("-")
        start, end = int(id_range[0]), int(id_range[1])
        for c in range(start, end+1):
            c_str = str(c)
            for partition in range(1, (len(c_str)//2) + 1):
                chunks = list(map(''.join, zip(*[iter(c_str)]*partition)))
                if len(chunks) < 2 or not chunks_valid(chunks, c_str):
                    continue
                if len(set(chunks)) == 1:
                    result += c
                    break
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
