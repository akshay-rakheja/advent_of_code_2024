from collections import defaultdict

# Global grid dimensions
GRID_WIDTH = 0
GRID_HEIGHT = 0


def read_input(filename="input.txt"):
    """Read the input file and return the map as a list of strings."""
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)


def find_antennas(grid):
    """Find all antennas and group them by frequency."""
    antennas = defaultdict(list)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            char = grid[y][x]
            if char != ".":
                antennas[char].append((x, y))
                print(f"Added antenna {char} at ({x}, {y})")
    return antennas


def get_direction(p1, p2):
    """Get the direction vector between two points if they form a valid line."""
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1

    # Check for valid line (horizontal, vertical, or any diagonal)
    if dx == 0 and dy != 0:  # vertical
        return (0, 1 if dy > 0 else -1)
    elif dy == 0 and dx != 0:  # horizontal
        return (1 if dx > 0 else -1, 0)
    else:  # any diagonal
        # Get the greatest common divisor to reduce the direction vector
        gcd = abs(dx)
        for i in range(abs(dx), 0, -1):
            if dx % i == 0 and dy % i == 0:
                gcd = i
                break
        # Return the simplified direction vector
        return (dx // gcd, dy // gcd)


def is_point_on_line(point, antenna1, antenna2):
    """Check if a point lies exactly on the line between two antennas."""
    px, py = point
    x1, y1 = antenna1
    x2, y2 = antenna2

    # Get direction vector
    direction = get_direction(antenna1, antenna2)
    dx, dy = direction

    # Check if point is reachable from antenna1 using the direction vector
    steps = 0
    x, y = x1, y1
    while 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        if (x, y) == (px, py):
            return True
        x += dx
        y += dy
        steps += 1
        # If we've gone past antenna2, stop
        if steps > max(GRID_WIDTH, GRID_HEIGHT):
            break

    return False


def find_antinodes(antenna_pair):
    """Find antinodes for a pair of antennas (any point in line with both)."""
    antenna1, antenna2 = antenna_pair
    x1, y1 = antenna1
    x2, y2 = antenna2

    # Get direction vector
    direction = get_direction(antenna1, antenna2)
    dx, dy = direction
    print(
        f"Found direction vector ({dx}, {dy}) between antennas at ({x1}, {y1}) and ({x2}, {y2})"
    )

    antinodes = set()

    # Check points in both directions from both antennas
    # From first antenna
    x, y = x1, y1
    # Forward direction
    while 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        antinodes.add((int(x), int(y)))
        x += dx
        y += dy

    # Backward direction
    x, y = x1 - dx, y1 - dy
    while 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        antinodes.add((int(x), int(y)))
        x -= dx
        y -= dy

    # From second antenna
    x, y = x2, y2
    # Forward direction
    while 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        antinodes.add((int(x), int(y)))
        x += dx
        y += dy

    # Backward direction
    x, y = x2 - dx, y2 - dy
    while 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        antinodes.add((int(x), int(y)))
        x -= dx
        y -= dy

    return antinodes


def find_all_antinodes(grid):
    """Find all antinode positions in the grid."""
    global GRID_WIDTH, GRID_HEIGHT
    GRID_HEIGHT = len(grid)
    GRID_WIDTH = len(grid[0])
    print(f"Grid dimensions: {GRID_WIDTH}x{GRID_HEIGHT}")

    antennas = find_antennas(grid)
    print("\nFound antennas:", antennas)
    all_antinodes = set()

    # For each frequency
    for freq, positions in antennas.items():
        print(f"\nChecking frequency {freq} with {len(positions)} antennas")
        # For each pair of antennas with the same frequency
        for i in range(len(positions)):
            print(f"Checking antenna {i} of {len(positions)}")
            for j in range(i + 1, len(positions)):
                print(f"Checking pair {i},{j}")
                # Create antenna pair and find its antinodes
                antenna_pair = (positions[i], positions[j])
                antinodes = find_antinodes(antenna_pair)
                if antinodes:
                    print(f"Found {len(antinodes)} antinodes for this pair")
                all_antinodes.update(antinodes)

    return all_antinodes


def create_visualization(grid, antinodes, antennas):
    """Create a visualization of the grid with antinodes marked."""
    # Convert grid to list of lists for modification
    viz_grid = [list(row) for row in grid]

    # Mark antinodes with '#'
    for x, y in antinodes:
        # Mark with '#' even if it's an antenna position
        viz_grid[y][x] = "#"

    # Convert back to strings
    return ["".join(row) for row in viz_grid]


def main():
    # Read input
    grid = read_input("day8/input.txt")
    print("Read input grid:")
    for row in grid:
        print(row)

    # Find all antinodes
    antinodes = find_all_antinodes(grid)
    antennas = find_antennas(grid)

    # Create visualization
    viz_grid = create_visualization(grid, antinodes, antennas)

    # Write visualization to file
    with open("day8/antinodes.txt", "w") as f:
        f.write("Original grid with antinodes marked as #:\n")
        f.write("(Antinodes now include antenna positions)\n\n")
        for row in viz_grid:
            f.write(row + "\n")
        f.write(f"\nTotal antinodes found: {len(antinodes)}")

    # Print only the count
    print(f"\nTotal antinodes found: {len(antinodes)}")


if __name__ == "__main__":
    main()
