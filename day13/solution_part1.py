import re
from typing import Tuple, Optional


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
                current_machine.append((numbers[0], numbers[1]))
                machines.append(tuple(current_machine))
                current_machine = []

    return machines


def find_min_tokens(
    button_a: Tuple[int, int],
    button_b: Tuple[int, int],
    prize: Tuple[int, int],
    max_presses: int = 100,
) -> Optional[int]:
    """
    Find minimum tokens needed to win the prize, or None if impossible.
    A button costs 3 tokens, B button costs 1 token.
    """
    # Try all combinations of button presses up to max_presses
    for a in range(max_presses + 1):
        for b in range(max_presses + 1):
            x = a * button_a[0] + b * button_b[0]
            y = a * button_a[1] + b * button_b[1]

            if x == prize[0] and y == prize[1]:
                return 3 * a + b  # Cost calculation

    return None  # No solution found


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
