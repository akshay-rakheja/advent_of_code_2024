from math import log10, floor
from collections import Counter


def read_input(filename="input.txt"):
    """Read the initial stone arrangement."""
    try:
        with open(f"day11/{filename}", "r") as file:
            # Store stones in a Counter for efficient counting and modification
            return Counter(int(x) for x in file.read().strip().split())
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)


def count_digits_cached():
    """Create a cached dictionary of digit counts for numbers up to 10000."""
    cache = {}
    for n in range(10000):
        if n == 0:
            cache[n] = 1
        else:
            cache[n] = floor(log10(n)) + 1
    return cache


def split_number_cached():
    """Create a cached dictionary of number splits."""
    splits = {}
    digit_counts = count_digits_cached()

    for n in range(10000):
        digits = digit_counts[n]
        if digits % 2 == 0:
            half_digits = digits // 2
            divisor = 10**half_digits
            splits[n] = (n // divisor, n % divisor)
    return splits


# Create global caches
DIGIT_COUNTS = count_digits_cached()
SPLITS = split_number_cached()


def count_digits(n):
    """Get digit count from cache or calculate for large numbers."""
    if n in DIGIT_COUNTS:
        return DIGIT_COUNTS[n]
    return floor(log10(n)) + 1 if n > 0 else 1


def transform_stones_fast(stones):
    """Transform stones using Counter and caches."""
    new_stones = Counter()

    for stone, count in stones.items():
        if stone == 0:
            # Rule 1: Replace 0 with 1
            new_stones[1] += count
        else:
            digits = count_digits(stone)
            if digits % 2 == 0:
                # Rule 2: Split into two stones
                if stone in SPLITS:
                    left, right = SPLITS[stone]
                else:
                    half_digits = digits // 2
                    divisor = 10**half_digits
                    left, right = stone // divisor, stone % divisor
                new_stones[left] += count
                new_stones[right] += count
            else:
                # Rule 3: Multiply by 2024
                new_stones[stone * 2024] += count

    return new_stones


def simulate_blinks_fast(stones, num_blinks, verbose=True):
    """Simulate blinking using optimized Counter operations."""
    current_stones = stones

    for blink in range(num_blinks):
        current_stones = transform_stones_fast(current_stones)
        stone_count = sum(current_stones.values())

        if verbose and (blink < 5 or blink % 10 == 9 or blink == num_blinks - 1):
            print(f"\nAfter {blink + 1} blinks:")
            print(f"Number of stones: {stone_count}")
            if blink < 5 and stone_count < 50:
                # Show actual stones for small counts
                stones_list = []
                for stone, count in sorted(current_stones.items()):
                    stones_list.extend([stone] * count)
                print("Stones:", " ".join(map(str, stones_list)))

    return current_stones


def main():
    # Test with example input first
    print("Testing with example input...")
    stones = read_input("test_input.txt")
    print(f"Initial stones: {sum(stones.values())}")

    # Simulate 6 blinks for test
    final_stones = simulate_blinks_fast(stones, 6, verbose=True)
    final_count = sum(final_stones.values())
    print(f"\nTest final number of stones: {final_count}")
    print("Expected number of stones: 22")

    # Now process actual input
    print("\nProcessing actual input...")
    stones = read_input("input.txt")
    print(f"Initial stones: {sum(stones.values())}")

    # Simulate 75 blinks
    final_stones = simulate_blinks_fast(stones, 75, verbose=True)
    print(f"\nFinal number of stones after 75 blinks: {sum(final_stones.values())}")


if __name__ == "__main__":
    main()
