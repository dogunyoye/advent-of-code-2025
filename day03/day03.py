import os.path

DATA = os.path.join(os.path.dirname(__file__), 'day03.txt')

# Brute force "try all pairs" solution
def part_one(data) -> int:
    result = 0
    lines = data.splitlines()
    for bank in lines:
        largest = -1
        for i in range(len(bank)):
            for j in range(i + 1, len(bank)):
                candidate = bank[i] + bank[j]
                largest = max(largest, int(candidate))
        result += largest
    return result


# Faster, "greedy" solution which finds the largest
# number within the bank (from left to right) that
# also leaves enough space (remaining numbers) to
# achieve our requirement of 12 numbers. This will
# give us the largest number we can make
def part_two(data) -> int:
    result = 0
    lines = data.splitlines()
    for bank in lines:
        joltages = [int(digit) for digit in bank]
        largest_number = []

        largest_idx = -1
        remaining = 12

        while remaining != 0:
            largest = -1
            for i in range(largest_idx + 1, len(joltages)):
                if joltages[i] > largest and (len(joltages) - i) >= remaining:
                    largest = joltages[i]
                    largest_idx = i
            largest_number.append(largest)
            remaining -= 1

        result += int(''.join(str(num) for num in largest_number))
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
