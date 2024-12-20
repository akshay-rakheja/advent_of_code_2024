def parse_input(filename):
    with open(filename) as f:
        patterns, designs = f.read().strip().split("\n\n")
        patterns = [p.strip() for p in patterns.split(",")]
        designs = designs.split("\n")
    return patterns, designs


def count_ways(design, patterns, memo=None):
    if memo is None:
        memo = {}

    if design == "":
        return 1  # Found one valid way

    if design in memo:
        return memo[design]

    total_ways = 0
    # Try each pattern at the current position
    for pattern in patterns:
        if design.startswith(pattern):
            # If pattern matches start of design, recursively count ways for the rest
            remaining = design[len(pattern) :]
            ways = count_ways(remaining, patterns, memo)
            total_ways += ways

    memo[design] = total_ways
    return total_ways


def solve_part2(filename):
    patterns, designs = parse_input(filename)

    # Sum up the number of ways each design can be made
    total_ways = sum(count_ways(design, patterns) for design in designs)

    return total_ways


if __name__ == "__main__":
    result = solve_part2("day19/input.txt")
    print(f"Total number of different ways: {result}")
