from typing import List, Tuple, Dict, Set
from collections import defaultdict
import heapq


def parse_input(filename: str) -> List[List[str]]:
    """Parse the input file into a 2D grid."""
    with open(filename, "r") as f:
        return [list(line.strip()) for line in f.readlines()]


def find_start_end(grid: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Find the start (S) and end (E) positions in the grid."""
    start = end = None
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "S":
                start = (y, x)
            elif grid[y][x] == "E":
                end = (y, x)
    return start, end


def get_rotation_cost(curr_dir: Tuple[int, int], new_dir: Tuple[int, int]) -> int:
    """Calculate rotation cost between two directions."""
    if curr_dir == new_dir:
        return 0

    # Map directions to compass points for easier rotation calculation
    dir_to_compass = {
        (0, 1): 0,  # East
        (1, 0): 1,  # South
        (0, -1): 2,  # West
        (-1, 0): 3,  # North
    }

    curr_compass = dir_to_compass[curr_dir]
    new_compass = dir_to_compass[new_dir]

    # Calculate minimum rotation (clockwise or counterclockwise)
    diff = abs(curr_compass - new_compass)
    if (
        diff == 3
    ):  # Special case: when diff is 3, it's actually a 90-degree turn in the other direction
        diff = 1

    return diff * 1000  # Each 90-degree rotation costs 1000


def get_neighbors(
    pos: Tuple[int, int], direction: Tuple[int, int], grid: List[List[str]]
) -> List[Tuple[Tuple[int, int], Tuple[int, int], int]]:
    """Get valid neighbors and their costs from current position and direction."""
    y, x = pos
    dy, dx = direction
    neighbors = []

    # All possible directions
    all_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # E, S, W, N

    for new_dy, new_dx in all_directions:
        new_y = y + new_dy
        new_x = x + new_dx

        # Check bounds and walls
        if (
            0 <= new_y < len(grid)
            and 0 <= new_x < len(grid[0])
            and grid[new_y][new_x] != "#"
        ):
            # Calculate total cost: rotation cost + movement cost
            rotation_cost = get_rotation_cost((dy, dx), (new_dy, new_dx))
            movement_cost = 1
            total_cost = rotation_cost + movement_cost

            neighbors.append(((new_y, new_x), (new_dy, new_dx), total_cost))

    return neighbors


def find_best_path_tiles(grid: List[List[str]]) -> Set[Tuple[int, int]]:
    """Find all tiles that are part of any best path through the maze using Dijkstra's algorithm."""
    start, end = find_start_end(grid)

    # Step 1: Find all best paths using Dijkstra's
    pq = [(0, start, (0, 1))]  # Start facing east
    costs = defaultdict(lambda: float("inf"))
    costs[(start, (0, 1))] = 0

    # Track predecessors to reconstruct paths
    predecessors = defaultdict(list)

    while pq:
        cost, pos, direction = heapq.heappop(pq)

        if cost > costs[(pos, direction)]:
            continue

        for next_pos, next_dir, move_cost in get_neighbors(pos, direction, grid):
            new_cost = cost + move_cost

            # If we found an equal or better path
            if new_cost <= costs[(next_pos, next_dir)]:
                # If it's a new best path, clear old predecessors
                if new_cost < costs[(next_pos, next_dir)]:
                    predecessors[(next_pos, next_dir)] = []

                # Record this path
                costs[(next_pos, next_dir)] = new_cost
                predecessors[(next_pos, next_dir)].append((pos, direction))
                heapq.heappush(pq, (new_cost, next_pos, next_dir))

    # Find the minimum cost to reach end
    min_end_cost = min(costs[(end, d)] for d in [(0, 1), (0, -1), (1, 0), (-1, 0)])

    # Step 2: Find all positions in best paths by backtracking from end
    best_path_tiles = set()
    to_visit = [
        (end, d)
        for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if costs[(end, d)] == min_end_cost
    ]
    visited = set()

    while to_visit:
        current_state = to_visit.pop()
        if current_state in visited:
            continue
        visited.add(current_state)

        pos, direction = current_state
        best_path_tiles.add(pos)  # Add this position to our set of best path tiles

        # Add all predecessors that lead to this state with minimum cost
        for prev_pos, prev_dir in predecessors[current_state]:
            if (
                costs[(prev_pos, prev_dir)] + get_rotation_cost(prev_dir, direction) + 1
                == costs[current_state]
            ):
                to_visit.append((prev_pos, prev_dir))

    # Step 3 & 4: Return the set of unique positions (duplicates automatically handled by set)
    return best_path_tiles


def print_grid_with_path(grid: List[List[str]], path_tiles: Set[Tuple[int, int]]):
    """Print the grid with path tiles marked as O."""
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (y, x) in path_tiles and grid[y][x] not in "SE":
                print("O", end="")
            else:
                print(grid[y][x], end="")
        print()


def solve(filename: str, debug: bool = False) -> int:
    """Main solution function."""
    grid = parse_input(filename)
    best_path_tiles = find_best_path_tiles(grid)

    if debug:
        print("\nGrid with best paths marked:")
        print_grid_with_path(grid, best_path_tiles)
        print()

    return len(best_path_tiles)


def test_solution():
    """Test the solution with example input."""
    test_result = solve("day16/test_input.txt", debug=True)
    print(f"Test result (number of tiles in best paths): {test_result}")

    if test_result == 45:  # Only proceed if test matches example
        print("\nRunning solution on full input...")
        result = solve("day16/input.txt")
        print(f"Solution: {result}")
    else:
        print(f"\nTest result {test_result} does not match expected value of 45.")


if __name__ == "__main__":
    test_solution()
