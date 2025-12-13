import os.path
import re

DATA = os.path.join(os.path.dirname(__file__), 'day12.txt')


def parse_input(text) -> tuple:
    patterns = {}
    sequences = {}

    lines = [line.rstrip() for line in text.splitlines() if line.strip()]

    i = 0
    while i < len(lines):
        line = lines[i]

        # --- Pattern block (e.g., "0:") ---
        if re.match(r"^\d+:\s*$", line):
            key = int(line[:-1])
            block = []

            # read following lines until next key or sequence
            i += 1
            while i < len(lines):
                if re.match(r"^\d+:\s*$", lines[i]) or re.match(r"^\S+:\s", lines[i]):
                    break
                block.append(list(lines[i]))
                i += 1

            patterns[key] = block
            continue

        # --- Sequence block (e.g., "4x4: 0 0 0 0 2 0") ---
        seq_match: re.Match = re.match(r"^(\S+):\s+(.*)$", line)
        if seq_match:
            label = seq_match.group(1)
            nums = list(map(int, seq_match.group(2).split()))
            if label in sequences:
                sequences[label].append(nums)
            else:
                sequences[label] = [nums]
            i += 1
            continue

        i += 1

    return patterns, sequences


def part_one(data: str) -> int:
    result = 0
    patterns, sequences = parse_input(data)
    for k, v, in sequences.items():
        dimensions = k.split("x")
        total_available_area = int(dimensions[0]) * int(dimensions[1])
        for vv in v:
            area_occupied_by_items = 0
            for idx, quantity in enumerate(vv):
                pattern = patterns[idx]
                item_area = 0
                for p in pattern:
                    item_area += p.count("#")
                area_occupied_by_items += item_area * quantity
            if total_available_area >= area_occupied_by_items:
                result += 1
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
