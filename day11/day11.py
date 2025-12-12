import os.path

DATA = os.path.join(os.path.dirname(__file__), 'day11.txt')


def __parse_devices(data) -> dict:
    devices = {}
    for line in data.splitlines():
        parts = line.split(': ')
        devices[parts[0]] = parts[1].split()
    return devices


def __traverse_devices(devices, output) -> int:
    if output == "out":
        return 1

    result = 0
    for o in devices[output]:
        result += __traverse_devices(devices, o)

    return result


def __traverse_devices_tracking_path(devices, output, dac, fft, memo) -> int:
    if output == "out":
        if dac and fft:
            return 1
        return 0

    state = (output, dac, fft)
    if state in memo:
        return memo[state]

    result = 0
    for o in devices[output]:
        found_dac = True if o == "dac" else dac
        found_fft = True if o == "fft" else fft
        result += __traverse_devices_tracking_path(devices, o, found_dac, found_fft, memo)

    memo[state] = result
    return result


def part_one(data) -> int:
    devices = __parse_devices(data)
    return __traverse_devices(devices, "you")


def part_two(data) -> int:
    devices = __parse_devices(data)
    return __traverse_devices_tracking_path(devices,"svr", False, False, {})


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
