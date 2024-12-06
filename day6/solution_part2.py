from collections import defaultdict


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


def simulate_guard_path_with_obstacle(grid, obstacle_x, obstacle_y, max_steps=10000):
    """Simulate guard path with an obstacle and detect loops."""
    if grid[obstacle_y][obstacle_x] != ".":
        return False

    # Create a modified grid with the obstacle
    modified_grid = [list(row) for row in grid]
    modified_grid[obstacle_y][obstacle_x] = "#"

    # Find guard's starting position
    start = find_guard_start(grid)
    if not start:
        return False

    x, y, direction = start
    visited = {}  # (x, y, direction) -> step
    path = []  # Store the path for loop verification
    step = 0

    while step < max_steps:
        next_x, next_y = get_next_position(x, y, direction)

        if not is_valid_position(next_x, next_y, modified_grid):
            return False

        if modified_grid[next_y][next_x] == "#":
            direction = turn_right(direction)
            state = (x, y, direction)
        else:
            x, y = next_x, next_y
            state = (x, y, direction)

        # Store the current state in the path
        path.append(state)

        # If we've seen this state before, check if it's a valid loop
        if state in visited:
            loop_start = visited[state]
            loop_length = step - loop_start

            # The loop must be at least 4 steps long (to form a proper cycle)
            # and must involve at least one turn (can't be just going back and forth)
            if loop_length >= 4:
                # Check if the loop contains at least one turn
                has_turn = False
                for i in range(loop_start, step):
                    if path[i][2] != path[i + 1][2]:  # Direction changed
                        has_turn = True
                        break
                if has_turn:
                    return True

        visited[state] = step
        step += 1

    return False


def find_loop_positions(grid):
    """Find all positions where placing an obstacle creates a loop."""
    loop_positions = set()

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "." and simulate_guard_path_with_obstacle(grid, x, y):
                loop_positions.add((x, y))

    return loop_positions


def main():
    # Read input
    grid = read_input("day6/input.txt")

    # Find all positions that create loops
    loop_positions = find_loop_positions(grid)

    # Print only the count
    print(len(loop_positions))


if __name__ == "__main__":
    main()
