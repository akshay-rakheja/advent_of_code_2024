from typing import List, Tuple, Dict
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


def find_shortest_path(grid: List[List[str]]) -> int:
    """Find the shortest path from S to E using Dijkstra's algorithm."""
    start, end = find_start_end(grid)

    # Priority queue: (total_cost, position, direction)
    # Start facing east as per problem description
    pq = [(0, start, (0, 1))]

    # Keep track of minimum cost to reach each state (position, direction)
    costs = defaultdict(lambda: float("inf"))
    costs[(start, (0, 1))] = 0

    while pq:
        total_cost, pos, direction = heapq.heappop(pq)

        # Skip if we've found a better path to this state
        if total_cost > costs[(pos, direction)]:
            continue

        # Check if we reached the end
        if pos == end:
            return total_cost

        # Try all possible moves
        for next_pos, next_dir, move_cost in get_neighbors(pos, direction, grid):
            new_cost = total_cost + move_cost

            # If we found a better path to this state
            if new_cost < costs[(next_pos, next_dir)]:
                costs[(next_pos, next_dir)] = new_cost
                heapq.heappush(pq, (new_cost, next_pos, next_dir))

    return float("inf")  # No path found


def solve(filename: str) -> int:
    """Main solution function."""
    grid = parse_input(filename)
    return find_shortest_path(grid)


def test_solution():
    """Test the solution with example input."""
    test_result = solve("day16/test_input.txt")
    print(f"Test result: {test_result}")

    # If test passes, run on actual input
    result = solve("day16/input.txt")
    print(f"Solution: {result}")


if __name__ == "__main__":
    test_solution()
