def read_input(filename="input.txt"):
    """Read the initial stone arrangement."""
    try:
        with open(f"day11/{filename}", "r") as file:
            return [int(x) for x in file.read().strip().split()]
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)


def has_even_digits(num):
    """Check if a number has an even number of digits."""
    return len(str(num)) % 2 == 0


def split_number(num):
    """Split a number into two halves."""
    num_str = str(num)
    mid = len(num_str) // 2
    left = int(num_str[:mid])
    right = int(num_str[mid:])
    return [left, right]


def transform_stones(stones):
    """Apply transformation rules to all stones."""
    new_stones = []

    for stone in stones:
        if stone == 0:
            # Rule 1: Replace 0 with 1
            new_stones.append(1)
        elif has_even_digits(stone):
            # Rule 2: Split into two stones
            new_stones.extend(split_number(stone))
        else:
            # Rule 3: Multiply by 2024
            new_stones.append(stone * 2024)

    return new_stones


def simulate_blinks(stones, num_blinks):
    """Simulate blinking num_blinks times."""
    current_stones = stones

    for blink in range(num_blinks):
        current_stones = transform_stones(current_stones)
        if blink < 5 or blink == num_blinks - 1:
            print(f"\nAfter {blink + 1} blinks:")
            print(f"Number of stones: {len(current_stones)}")
            if len(current_stones) < 20:
                print("Stones:", " ".join(map(str, current_stones)))

    return current_stones


def main():
    # Test with example input first
    print("Testing with example input...")
    stones = read_input("test_input.txt")
    print(f"Initial stones: {' '.join(map(str, stones))}")
    print(f"Initial number of stones: {len(stones)}")

    # Simulate 6 blinks for test
    final_stones = simulate_blinks(stones, 6)
    print(f"\nTest final number of stones: {len(final_stones)}")
    print("Expected number of stones: 22")

    # Now process actual input
    print("\nProcessing actual input...")
    stones = read_input("input.txt")
    print(f"Initial stones: {' '.join(map(str, stones))}")
    print(f"Initial number of stones: {len(stones)}")

    # Simulate 25 blinks
    final_stones = simulate_blinks(stones, 25)
    print(f"\nFinal number of stones: {len(final_stones)}")


if __name__ == "__main__":
    main()
