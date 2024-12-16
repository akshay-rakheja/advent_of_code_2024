import re
from typing import Tuple, Optional
from math import gcd
from dataclasses import dataclass

OFFSET = 10_000_000_000_000


@dataclass
class Machine:
    button_a: Tuple[int, int]
    button_b: Tuple[int, int]
    prize: Tuple[int, int]


def parse_line(line: str) -> Tuple[int, int]:
    """Parse a line containing X and Y coordinates."""
    x_match = re.search(r"X([+=])(-?\d+)", line)
    y_match = re.search(r"Y([+=])(-?\d+)", line)

    if not x_match or not y_match:
        raise ValueError(f"Invalid line format: {line}")

    x_val = int(x_match.group(2))
    y_val = int(y_match.group(2))

    return (x_val, y_val)


def parse_input(filename: str) -> list[Machine]:
    machines = []
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    for i in range(0, len(lines), 3):
        button_a = parse_line(lines[i])
        button_b = parse_line(lines[i + 1])
        prize = parse_line(lines[i + 2])
        machines.append(Machine(button_a=button_a, button_b=button_b, prize=prize))

    return machines


def solve_diophantine(a: int, b: int, c: int) -> Optional[Tuple[int, int]]:
    """
    Solves the Diophantine equation: ax + by = c
    Returns the solution with minimum non-negative x and y, or None if no solution exists
    """
    if a == 0 and b == 0:
        return (0, 0) if c == 0 else None

    g = gcd(abs(a), abs(b))
    if c % g != 0:
        return None

    # Scale down the equation
    a, b, c = a // g, b // g, c // g

    # Base solution using extended Euclidean algorithm
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if b == 0:
            return a, 1, 0
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y

    _, x0, y0 = extended_gcd(abs(a), abs(b))
    x0 *= -1 if a < 0 else 1
    y0 *= -1 if b < 0 else 1
    x0 *= c
    y0 *= c

    # Find minimum non-negative solution
    if b < 0:
        k = -(x0 // b) if x0 > 0 else (-x0 + abs(b) - 1) // abs(b)
    else:
        k = -(x0 // b) if x0 < 0 else 0

    x = x0 + b * k
    y = y0 - a * k

    while x < 0 or y < 0:
        if b > 0:
            k += 1
        else:
            k -= 1
        x = x0 + b * k
        y = y0 - a * k

    return (x, y)


def find_min_tokens(machine: Machine) -> Optional[int]:
    """
    Find minimum tokens needed to win the prize, or None if impossible.
    Optimized version with early validation and efficient calculations.
    """
    dx1, dy1 = machine.button_a
    dx2, dy2 = machine.button_b
    target_x, target_y = machine.prize[0], machine.prize[1]

    # Early validation
    if dx1 == 0 and dx2 == 0:
        return None
    if dy1 == 0 and dy2 == 0:
        return None

    # We need to solve:
    # a * dx1 + b * dx2 = target_x - OFFSET
    # a * dy1 + b * dy2 = target_y - OFFSET
    # where a and b are non-negative integers

    # Try to find a solution for x coordinate
    solution_x = solve_diophantine(dx1, dx2, target_x - OFFSET)
    if solution_x is None:
        return None

    a, b = solution_x

    # Verify y coordinate
    if a * dy1 + b * dy2 != target_y - OFFSET:
        # Try to find alternative solutions by adding multiples of dx2/gcd to a
        # and subtracting multiples of dx1/gcd from b
        g = gcd(abs(dx1), abs(dx2))
        step_a = abs(dx2) // g
        step_b = abs(dx1) // g

        # Try a few steps in both directions
        for k in range(-1000, 1001):  # Reasonable range to try
            new_a = a + k * step_a
            new_b = b - k * (step_b if dx1 * dx2 > 0 else -step_b)

            if new_a >= 0 and new_b >= 0:
                if new_a * dy1 + new_b * dy2 == target_y - OFFSET:
                    a, b = new_a, new_b
                    break
        else:
            return None

    return 3 * a + b


def main(test_mode: bool = False):
    filename = "day13/test_input.txt" if test_mode else "day13/input.txt"
    machines = parse_input(filename)
    total_tokens = 0
    winnable_prizes = 0

    for i, machine in enumerate(machines, 1):
        tokens = find_min_tokens(machine)
        if tokens is not None:
            total_tokens += tokens
            winnable_prizes += 1
            print(f"Machine {i}: Winnable with {tokens} tokens")
        else:
            print(f"Machine {i}: Not winnable")

    print(f"\nNumber of winnable prizes: {winnable_prizes}")
    print(f"Total tokens needed: {total_tokens}")

    if test_mode:
        # In the example, only machines 2 and 4 are winnable
        assert (
            winnable_prizes == 2
        ), f"Expected 2 winnable prizes, got {winnable_prizes}"


if __name__ == "__main__":
    # Run with test data first
    print("Running tests...")
    main(test_mode=True)
    print("\nRunning with actual input...")
    main(test_mode=False)
