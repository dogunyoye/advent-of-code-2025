import os.path
from collections import deque
from fractions import Fraction
from itertools import product
from math import gcd

DATA = os.path.join(os.path.dirname(__file__), 'day10.txt')


class Machine(object):

    def __init__(self, light_diagram, light_diagram_length, buttons, joltage_requirements):
        self.light_diagram = light_diagram
        self.light_diagram_length = light_diagram_length
        self.buttons = buttons
        self.joltage_requirements = joltage_requirements


def __encode_to_bitmask(pattern: str) -> int:
    bitmask = 0
    for ch in pattern:
        bitmask <<= 1              # shift left to make room
        if ch == '#':
            bitmask |= 1           # set the lowest bit
        elif ch != '.':
            raise ValueError(f"Invalid character: {ch}")
    return bitmask


def __parse_machines(data) -> list[Machine]:
    machines = []
    for line in data.splitlines():
        parts = line.split()
        light_diagram_list = list(parts[0][1:len(parts[0])-1])
        light_diagram = __encode_to_bitmask("".join(light_diagram_list))
        joltage_requirements = list(map(int, parts[-1][1:len(parts[-1])-1].split(",")))
        buttons = []
        for b in parts[1:-1]:
            nums = []
            for n in b[1:-1].split(","):
                nums.append(int(n))
            buttons.append(nums)
        machines.append(Machine(light_diagram, len(light_diagram_list), buttons, joltage_requirements))
    return machines


def __toggle(diagram, button, length) -> int:
    new_diagram = diagram
    for pos in button:
        new_diagram ^= (1 << length - 1 - pos) # left to right indexing
    return new_diagram


def __bfs(machine) -> int:
    queue = deque()
    visited = set()
    queue.append((0, 0))

    while len(queue) != 0:
        current_diagram, current_steps = queue.popleft()

        if current_diagram == machine.light_diagram:
            return current_steps

        for button in machine.buttons:
            next_diagram = __toggle(current_diagram, button, machine.light_diagram_length)
            if next_diagram not in visited:
                visited.add(next_diagram)
                queue.append((next_diagram, current_steps + 1))

    raise Exception("No solution")


def __build_matrix(targets, buttons) -> list:
    """A[i][j] = amount counter i is incremented by pressing button j once."""
    matrix = [[0] * len(buttons) for _ in targets]
    for j, button in enumerate(buttons):
        for counter in button:
            matrix[counter][j] += 1
    return matrix


def __reduced_row_echelon(matrix, targets) -> tuple | None:
    """Exact RREF of the augmented system ``matrix @ x = targets``.

    Returns ``(rows, pivot_columns)`` where ``rows[i][n]`` is the right-hand
    side, or ``None`` if the system is inconsistent.
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    aug = [[Fraction(matrix[i][j]) for j in range(cols)] + [Fraction(targets[i])] for i in range(rows)]

    pivot_columns = []
    r = 0
    for c in range(cols):
        pivot_row = None
        for i in range(r, rows):
            if aug[i][c] != 0:
                pivot_row = i
                break
        if pivot_row is None:
            continue

        aug[r], aug[pivot_row] = aug[pivot_row], aug[r]
        pivot_value = aug[r][c]
        aug[r] = [value / pivot_value for value in aug[r]]

        for i in range(rows):
            if i != r and aug[i][c] != 0:
                factor = aug[i][c]
                aug[i] = [a - factor * b for a, b in zip(aug[i], aug[r])]

        pivot_columns.append(c)
        r += 1
        if r == rows:
            break

    for i in range(r, rows):
        if any(aug[i][c] != 0 for c in range(cols)) or aug[i][cols] != 0:
            return None

    return aug, pivot_columns


def __lcm(a, b) -> int:
    return a // gcd(a, b) * b


def __min_presses(targets, buttons) -> int:
    """Fewest total presses so that ``A @ x = targets`` with ``x >= 0`` integer.

    The system is small (<= 10 counters, <= 13 buttons) and its null space has
    dimension <= 3, so after exact Gaussian elimination we can enumerate the
    free variables. Every ``x_j`` is bounded by the smallest joltage it
    contributes to, so the enumeration is tiny.
    """
    matrix = __build_matrix(targets, buttons)
    reduced = __reduced_row_echelon(matrix, targets)
    if reduced is None:
        raise Exception("Infeasible machine")

    rows, pivot_columns = reduced
    pivot_set = set(pivot_columns)
    free_columns = [c for c in range(len(buttons)) if c not in pivot_set]

    ranges = []
    for f in free_columns:
        bound = min(targets[c] for c in buttons[f]) if buttons[f] else 0
        ranges.append(range(bound + 1))

    # Express each pivot variable as ``(rhs - sum(coeff * free)) / denom`` using
    # integers, so the inner loop never touches Fraction.
    pivot_terms = []
    for i in range(len(pivot_columns)):
        row = rows[i]
        denom = 1
        for c in range(len(buttons) + 1):
            denom = __lcm(denom, row[c].denominator)
        rhs = int(row[len(buttons)] * denom)
        terms = [(pos, int(row[f] * denom)) for pos, f in enumerate(free_columns) if row[f] != 0]
        pivot_terms.append((rhs, denom, terms))

    best = None
    for free_values in product(*ranges):
        total = sum(free_values)
        feasible = True
        for rhs, denom, terms in pivot_terms:
            value = rhs
            for pos, coeff in terms:
                value -= coeff * free_values[pos]
            if value < 0 or value % denom != 0:
                feasible = False
                break
            total += value // denom
        if feasible and (best is None or total < best):
            best = total

    if best is None:
        raise Exception("Infeasible machine")
    return best


def part_one(data) -> int:
    result = 0
    machines = __parse_machines(data)
    for machine in machines:
        result += __bfs(machine)
    return result


def part_two(data) -> int:
    answer = 0
    machines = __parse_machines(data)
    for machine in machines:
        answer += __min_presses(machine.joltage_requirements, machine.buttons)
    return answer


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
