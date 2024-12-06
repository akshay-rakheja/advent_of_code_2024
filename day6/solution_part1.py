def read_input(filename="input.txt"):
    """Read the input file and return the map as a list of strings."""
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)


def find_guard_start(grid):
    """Find the guard's starting position and direction."""
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "^":
                return x, y, "up"
            elif grid[y][x] == ">":
                return x, y, "right"
            elif grid[y][x] == "v":
                return x, y, "down"
            elif grid[y][x] == "<":
                return x, y, "left"
    return None


def get_next_position(x, y, direction):
    """Get the next position based on current direction."""
    if direction == "up":
        return x, y - 1
    elif direction == "right":
        return x + 1, y
    elif direction == "down":
        return x, y + 1
    else:  # left
        return x - 1, y


def turn_right(direction):
    """Return the new direction after turning right."""
    directions = ["up", "right", "down", "left"]
    current_index = directions.index(direction)
    return directions[(current_index + 1) % 4]


def is_valid_position(x, y, grid):
    """Check if position is within grid bounds."""
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def simulate_guard_path(grid):
    """Simulate the guard's movement and return set of visited positions."""
    # Find guard's starting position
    start = find_guard_start(grid)
    if not start:
        return set()

    x, y, direction = start
    visited = {(x, y)}  # Set of visited positions

    while True:
        # Get position in front
        next_x, next_y = get_next_position(x, y, direction)

        # Check if guard would leave the area
        if not is_valid_position(next_x, next_y, grid):
            break

        # Check if there's an obstacle in front
        if grid[next_y][next_x] == "#":
            # Turn right
            direction = turn_right(direction)
        else:
            # Move forward
            x, y = next_x, next_y
            visited.add((x, y))

    return visited


def main():
    # Read input
    grid = read_input("day6/input.txt")

    # Simulate guard's path
    visited = simulate_guard_path(grid)

    # Print only the count of distinct positions
    print(len(visited))


if __name__ == "__main__":
    main()
