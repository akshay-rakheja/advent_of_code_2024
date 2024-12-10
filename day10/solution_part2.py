from collections import deque


def read_input(filename="input.txt"):
    """Read the topographic map from input file."""
    try:
        with open(f"day10/{filename}", "r") as file:
            return [list(map(int, line.strip())) for line in file]
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)


def find_trailheads(topo_map):
    """Find all positions with height 0 (trailheads)."""
    rows, cols = len(topo_map), len(topo_map[0])
    trailheads = []
    for r in range(rows):
        for c in range(cols):
            if topo_map[r][c] == 0:
                trailheads.append((r, c))
    return trailheads


def get_neighbors(pos, rows, cols):
    """Get valid neighboring positions (up, down, left, right)."""
    r, c = pos
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # up, down, left, right
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < rows and 0 <= new_c < cols:
            neighbors.append((new_r, new_c))
    return neighbors


def count_distinct_trails(topo_map, start):
    """Count distinct hiking trails from start to any height 9."""
    rows, cols = len(topo_map), len(topo_map[0])
    distinct_trails = set()  # Store unique paths to height 9
    queue = deque([(start, tuple([start]))])  # (position, path)

    while queue:
        pos, path = queue.popleft()
        r, c = pos
        current_height = topo_map[r][c]

        if current_height == 9:
            # Found a valid trail, add it to distinct trails
            distinct_trails.add(path)
            continue

        for next_pos in get_neighbors(pos, rows, cols):
            nr, nc = next_pos
            next_height = topo_map[nr][nc]

            # Check if it's a valid step (height increases by exactly 1)
            if next_height == current_height + 1 and next_pos not in path:
                # Create new path by appending next position
                new_path = path + (next_pos,)
                queue.append((next_pos, new_path))

    return len(distinct_trails)


def calculate_total_rating(topo_map):
    """Calculate the sum of ratings for all trailheads."""
    trailheads = find_trailheads(topo_map)
    total_rating = 0

    print(f"Found {len(trailheads)} trailheads")
    for i, trailhead in enumerate(trailheads, 1):
        rating = count_distinct_trails(topo_map, trailhead)
        print(f"Trailhead {i} at {trailhead}: rating = {rating}")
        total_rating += rating

    return total_rating


def main():
    # Test with example input first
    print("Testing with example input...")
    topo_map = read_input("test_input.txt")
    print(f"Map dimensions: {len(topo_map)}x{len(topo_map[0])}")

    # Calculate total rating for test
    total_rating = calculate_total_rating(topo_map)
    print(f"\nTest total rating: {total_rating}")
    print("Expected rating: 81")

    # Now process actual input
    print("\nProcessing actual input...")
    topo_map = read_input("input.txt")
    print(f"Map dimensions: {len(topo_map)}x{len(topo_map[0])}")

    # Calculate total rating
    total_rating = calculate_total_rating(topo_map)
    print(f"\nFinal total rating: {total_rating}")


if __name__ == "__main__":
    main()
