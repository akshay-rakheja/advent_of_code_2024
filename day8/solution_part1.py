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


def find_antinodes(antenna_pair):
    """Find antinodes for a pair of antennas."""
    antenna1, antenna2 = antenna_pair
    x1, y1 = antenna1
    x2, y2 = antenna2

    # Get direction vector
    direction = get_direction(antenna1, antenna2)
    if direction is None:  # Not a valid line
        print(f"No valid line between antennas at ({x1}, {y1}) and ({x2}, {y2})")
        return []

    dx, dy = direction
    print(
        f"Found direction vector ({dx}, {dy}) between antennas at ({x1}, {y1}) and ({x2}, {y2})"
    )
    antinodes = set()

    # Calculate distance between antennas
    antenna_dist = max(abs(x2 - x1), abs(y2 - y1))
    print(f"Distance between antennas: {antenna_dist}")

    # Check points along the line (including before and after antennas)
    # We'll check up to twice the antenna distance in both directions
    for d in range(-2 * antenna_dist, 2 * antenna_dist + 1):
        # Check point at position d steps from antenna1
        x = x1 + dx * d
        y = y1 + dy * d

        # Skip if out of bounds
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            continue

        # Calculate distances to both antennas
        dist1 = max(abs(x - x1), abs(y - y1))
        dist2 = max(abs(x - x2), abs(y - y2))

        # Check if this is an antinode (one distance is twice the other)
        if dist1 > 0 and dist2 > 0:
            if dist1 == 2 * dist2 or dist2 == 2 * dist1:
                antinodes.add((int(x), int(y)))
                print(
                    f"Found antinode at ({int(x)}, {int(y)}) with distances {dist1} and {dist2}"
                )

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
        # Only mark if not an antenna
        if viz_grid[y][x] == ".":
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
        f.write("(Antinodes at antenna positions are not marked)\n\n")
        for row in viz_grid:
            f.write(row + "\n")
        f.write(f"\nTotal antinodes found: {len(antinodes)}")

    # Print only the count
    print(f"\nTotal antinodes found: {len(antinodes)}")


if __name__ == "__main__":
    main()
