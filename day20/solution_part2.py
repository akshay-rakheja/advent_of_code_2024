from collections import deque
from typing import List, Tuple, Set, Dict


def parse_input(
    filename: str,
) -> Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
    grid = []
    start = None
    end = None

    with open(filename) as f:
        for i, line in enumerate(f):
            row = list(line.strip())
            for j, char in enumerate(row):
                if char == "S":
                    start = (i, j)
                    row[j] = "."
                elif char == "E":
                    end = (i, j)
                    row[j] = "."
            grid.append(row)

    return grid, start, end


def get_neighbors(
    pos: Tuple[int, int], grid: List[List[str]], allow_walls: bool = False
) -> List[Tuple[int, int]]:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r, c = pos
    neighbors = []

    for dr, dc in directions:
        new_r, new_c = r + dr, c + dc
        if (
            0 <= new_r < len(grid)
            and 0 <= new_c < len(grid[0])
            and (
                grid[new_r][new_c] == "." or (allow_walls and grid[new_r][new_c] == "#")
            )
        ):
            neighbors.append((new_r, new_c))

    return neighbors


def bfs_distances(
    grid: List[List[str]], start: Tuple[int, int]
) -> Dict[Tuple[int, int], int]:
    """Calculate distances from start to all reachable points using BFS"""
    distances = {start: 0}
    queue = deque([start])

    while queue:
        pos = queue.popleft()
        for next_pos in get_neighbors(pos, grid):
            if next_pos not in distances:
                distances[next_pos] = distances[pos] + 1
                queue.append(next_pos)

    return distances


def get_valid_cheat_paths(
    pos: Tuple[int, int], grid: List[List[str]], max_steps: int = 20
) -> Dict[Tuple[int, int], int]:
    """Find all valid positions reachable within max_steps, allowing wall passing.
    Returns a dictionary mapping end positions to minimum steps needed."""
    valid_ends = {}  # (r, c) -> min_steps
    queue = deque([(pos, 0)])  # (position, steps)
    seen = {pos: 0}  # position -> min steps seen

    while queue:
        (r, c), steps = queue.popleft()
        if steps > 0 and grid[r][c] == ".":
            if (r, c) not in valid_ends or steps < valid_ends[(r, c)]:
                valid_ends[(r, c)] = steps

        if steps < max_steps:
            for new_r, new_c in get_neighbors((r, c), grid, allow_walls=True):
                if (new_r, new_c) not in seen or steps + 1 < seen[(new_r, new_c)]:
                    seen[(new_r, new_c)] = steps + 1
                    queue.append(((new_r, new_c), steps + 1))

    return valid_ends


def find_cheats(
    grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]
) -> int:
    # Calculate distances from start and end to all reachable points
    forward_distances = bfs_distances(grid, start)
    backward_distances = bfs_distances(grid, end)

    if end not in forward_distances:
        return 0  # No path exists

    normal_dist = forward_distances[end]
    cheats_100plus = set()  # Use set to avoid duplicates

    # For each reachable point, try it as a cheat start position
    for cheat_start in forward_distances:
        # Get all valid cheat end positions from this start and their minimum steps
        cheat_ends = get_valid_cheat_paths(cheat_start, grid)

        # For each valid end position
        for cheat_end, cheat_steps in cheat_ends.items():
            # Check if we can reach the final destination from here
            if cheat_end in backward_distances:
                # Calculate total distance with this cheat
                cheat_dist = (
                    forward_distances[cheat_start]  # Distance to cheat start
                    + cheat_steps  # Steps used during cheat
                    + backward_distances[cheat_end]  # Distance from cheat end to finish
                )

                if cheat_dist < normal_dist:
                    saved = normal_dist - cheat_dist
                    if saved >= 100:
                        # Store the cheat uniquely by its start and end positions
                        cheats_100plus.add((cheat_start, cheat_end))

    return len(cheats_100plus)


def main():
    grid, start, end = parse_input("day20/input.txt")
    result = find_cheats(grid, start, end)
    print(f"Number of cheats saving at least 100 picoseconds: {result}")


if __name__ == "__main__":
    main()
