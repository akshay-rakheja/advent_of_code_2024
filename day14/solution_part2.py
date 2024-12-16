from solution_part1 import parse_input, simulate_step


def is_christmas_tree_pattern(robots, width, height):
    # Create a grid to visualize robot positions
    grid = [[0] * width for _ in range(height)]
    for (x, y), _ in robots:
        grid[y][x] += 1

    # Count total robots
    total_robots = len(robots)
    robots_in_pattern = 0

    # Look for a triangular pattern that resembles a Christmas tree
    # The pattern should be roughly centered and have more robots at the bottom
    center_x = width // 2
    center_y = height // 2

    # Check if there's a higher concentration of robots in a triangular shape
    # around the center of the grid
    for y in range(height):
        for x in range(width):
            if grid[y][x] > 0:
                # Calculate distance from center
                dx = abs(x - center_x)
                dy = abs(y - center_y)

                # Check if this robot is part of a triangular shape
                # The further down we go, the wider the acceptable range
                max_width = dy + 5  # Allow for some spread at the bottom
                if dx <= max_width:
                    robots_in_pattern += grid[y][x]

    # If a significant portion of robots are in a tree-like pattern
    # This threshold might need tuning
    return robots_in_pattern > total_robots * 0.8


def solve(input_file):
    robots = parse_input(input_file)
    width, height = 101, 103

    seconds = 0
    max_seconds = 1000000  # Prevent infinite loop

    while seconds < max_seconds:
        if is_christmas_tree_pattern(robots, width, height):
            return seconds

        robots = simulate_step(robots, width, height)
        seconds += 1

    return "Pattern not found within time limit"


if __name__ == "__main__":
    result = solve("day14/input.txt")
    print(f"Christmas tree pattern appears after {result} seconds")
