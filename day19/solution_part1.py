def parse_input(filename):
    with open(filename) as f:
        patterns, designs = f.read().strip().split("\n\n")
        patterns = [p.strip() for p in patterns.split(",")]
        designs = designs.split("\n")
    return patterns, designs


def can_make_design(design, patterns, memo=None):
    if memo is None:
        memo = {}

    if design == "":
        return True

    if design in memo:
        return memo[design]

    # Try each pattern at the current position
    for pattern in patterns:
        if design.startswith(pattern):
            # If pattern matches start of design, recursively try to match the rest
            remaining = design[len(pattern) :]
            if can_make_design(remaining, patterns, memo):
                memo[design] = True
                return True

    memo[design] = False
    return False


def solve_part1(filename):
    patterns, designs = parse_input(filename)

    # Count how many designs are possible
    possible_count = sum(1 for design in designs if can_make_design(design, patterns))

    return possible_count


if __name__ == "__main__":
    result = solve_part1("day19/input.txt")
    print(f"Number of possible designs: {result}")
