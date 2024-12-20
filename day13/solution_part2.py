import re
from typing import Tuple, Optional

OFFSET = 10000000000000  # The offset added to prize coordinates


def parse_input(
    filename: str,
) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    machines = []
    current_machine = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Extract numbers using regex
            numbers = [int(x) for x in re.findall(r"-?\d+", line)]

            if line.startswith("Button A"):
                current_machine = [(numbers[0], numbers[1])]
            elif line.startswith("Button B"):
                current_machine.append((numbers[0], numbers[1]))
            elif line.startswith("Prize"):
                # Add the offset to prize coordinates
                prize_x = numbers[0] + OFFSET
                prize_y = numbers[1] + OFFSET
                current_machine.append((prize_x, prize_y))
                machines.append(tuple(current_machine))
                current_machine = []

    return machines


def find_min_tokens(
    button_a: Tuple[int, int],
    button_b: Tuple[int, int],
    prize: Tuple[int, int],
) -> Optional[int]:
    """
    Find minimum tokens needed to win the prize, or None if impossible.
    A button costs 3 tokens, B button costs 1 token.
    """
    # We need to solve:
    # a * button_a[0] + b * button_b[0] = prize[0]
    # a * button_a[1] + b * button_b[1] = prize[1]

    # Using Cramer's rule to solve for a and b
    determinant = button_a[0] * button_b[1] - button_a[1] * button_b[0]

    if determinant == 0:
        return None  # No unique solution exists

    # Solve for a and b
    a = (prize[0] * button_b[1] - prize[1] * button_b[0]) / determinant
    b = (button_a[0] * prize[1] - button_a[1] * prize[0]) / determinant

    # Check if a and b are non-negative integers
    if a >= 0 and b >= 0 and a.is_integer() and b.is_integer():
        return 3 * int(a) + int(b)  # Cost calculation

    return None  # No valid solution


def main():
    machines = parse_input("day13/input.txt")
    total_tokens = 0
    winnable_prizes = 0

    for i, (button_a, button_b, prize) in enumerate(machines, 1):
        tokens = find_min_tokens(button_a, button_b, prize)
        if tokens is not None:
            total_tokens += tokens
            winnable_prizes += 1
            print(f"Machine {i}: Winnable with {tokens} tokens")
        else:
            print(f"Machine {i}: Not winnable")

    print(f"\nNumber of winnable prizes: {winnable_prizes}")
    print(f"Total tokens needed: {total_tokens}")


if __name__ == "__main__":
    main()
