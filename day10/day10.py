import os.path
from collections import deque

from z3 import Int, Sum, sat, IntVal, Optimize

DATA = os.path.join(os.path.dirname(__file__), 'day10.txt')


class Machine(object):

    def __init__(self, light_diagram, buttons, joltage_requirements):
        self.light_diagram = light_diagram
        self.buttons = buttons
        self.joltage_requirements = joltage_requirements


def __parse_machines(data) -> list[Machine]:
    machines = []
    for line in data.splitlines():
        parts = line.split()
        light_diagram = list(parts[0][1:len(parts[0])-1])
        joltage_requirements = list(map(int, parts[-1][1:len(parts[-1])-1].split(",")))
        buttons = []
        for b in parts[1:-1]:
            nums = []
            for n in b[1:-1].split(","):
                nums.append(int(n))
            buttons.append(nums)
        machines.append(Machine(light_diagram, buttons, joltage_requirements))
    return machines


def __toggle(diagram, button) -> list:
    new_diagram = []
    for l in diagram:
        new_diagram.append(l)

    for b in button:
        v = new_diagram[b]
        if v == ".":
            new_diagram[b] = "#"
        elif v == "#":
            new_diagram[b] = "."
    return new_diagram


def __bfs(machine) -> int:
    queue = deque()
    visited = set()
    visited.add("".join(["."] * len(machine.light_diagram)))
    for b in machine.buttons:
        initial_diagram = ["."] * len(machine.light_diagram)
        queue.append((initial_diagram, b, 0))

    while len(queue) != 0:
        current_diagram, current_button, current_steps = queue.popleft()

        if current_diagram == machine.light_diagram:
            return current_steps

        for b in machine.buttons:
            toggled = __toggle(current_diagram, b)
            if "".join(toggled) not in visited:
                visited.add("".join(toggled))
                queue.append((toggled, b, current_steps + 1))

    raise Exception("No solution")


def part_one(data) -> int:
    result = 0
    machines = __parse_machines(data)
    for i, m in enumerate(machines):
        result += __bfs(m)
    return result


def part_two(data) -> int:
    answer = 0
    machines = __parse_machines(data)
    for m in machines:
        # AI assisted Z3 solution
        n_moves = len(m.buttons)
        n_states = len(m.joltage_requirements)

        # Build increment matrix A[i][j] = how much move j increments state i
        A = [[0] * n_moves for _ in range(n_states)]
        for j, mv in enumerate(m.buttons):
            for s in mv:
                A[s][j] += 1

        # Variables: x[j] = number of times we apply move j
        x = [Int(f"x{j}") for j in range(n_moves)]

        # Use Optimize ONLY if we minimize; otherwise simple Solver()
        solver = Optimize()

        # Non-negative integers
        for var in x:
            solver.add(var >= 0)

        # Upper bounds to prevent Z3 from wandering into infinity
        # Max value needed for any move can't exceed max(target)
        MAX_T = max(m.joltage_requirements)
        for var in x:
            solver.add(var <= MAX_T)

        # Ax = target
        for i in range(n_states):
            # IMPORTANT: use IntVal to avoid Python-int mixing
            solver.add(
                Sum([IntVal(A[i][j]) * x[j] for j in range(n_moves)]) == IntVal(m.joltage_requirements[i])
            )

        solver.minimize(Sum(x))

        # Solve
        result = solver.check()
        if result != sat:
            return -1  # infeasible

        model = solver.model()
        counts = [model[v].as_long() for v in x]
        answer += sum(counts)
    return answer


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
