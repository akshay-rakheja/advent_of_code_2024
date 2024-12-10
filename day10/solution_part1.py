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


def find_reachable_nines(topo_map, start):
    """Find all height-9 positions reachable via valid hiking trails from start."""
    rows, cols = len(topo_map), len(topo_map[0])
    visited = set()
    reachable_nines = set()
    queue = deque([(start, {start})])  # (position, path)

    while queue:
        pos, path = queue.popleft()
        r, c = pos
        current_height = topo_map[r][c]

        if current_height == 9:
            reachable_nines.add(pos)
            continue

        for next_pos in get_neighbors(pos, rows, cols):
            nr, nc = next_pos
            next_height = topo_map[nr][nc]

            # Check if it's a valid step (height increases by exactly 1)
            if next_height == current_height + 1 and next_pos not in path:
                new_path = path | {next_pos}
                path_key = (next_pos, tuple(sorted(new_path)))

                if path_key not in visited:
                    visited.add(path_key)
                    queue.append((next_pos, new_path))

    return len(reachable_nines)


def calculate_total_score(topo_map):
    """Calculate the sum of scores for all trailheads."""
    trailheads = find_trailheads(topo_map)
    total_score = 0

    print(f"Found {len(trailheads)} trailheads")
    for i, trailhead in enumerate(trailheads, 1):
        score = find_reachable_nines(topo_map, trailhead)
        print(f"Trailhead {i} at {trailhead}: score = {score}")
        total_score += score

    return total_score


def main():
    # Read and process input
    print("Reading topographic map...")
    topo_map = read_input("input.txt")
    print(f"Map dimensions: {len(topo_map)}x{len(topo_map[0])}")

    # Calculate total score
    total_score = calculate_total_score(topo_map)
    print(f"\nTotal score: {total_score}")


if __name__ == "__main__":
    main()
