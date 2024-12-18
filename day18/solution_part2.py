from collections import deque
import heapq


def parse_input(file_path):
    coordinates = []
    with open(file_path, "r") as f:
        for line in f:
            x, y = map(int, line.strip().split(","))
            coordinates.append((x, y))
    return coordinates


def create_grid(coordinates, max_size=71):
    grid = [["."] * max_size for _ in range(max_size)]
    for x, y in coordinates:
        grid[y][x] = "#"
    return grid


def print_grid(grid):
    for row in grid:
        print("".join(row))


def has_path_to_exit(grid):
    rows, cols = len(grid), len(grid[0])
    start = (0, 0)
    end = (cols - 1, rows - 1)

    # If start or end is blocked, no path exists
    if grid[start[1]][start[0]] == "#" or grid[end[1]][end[0]] == "#":
        return False

    # Use BFS for faster path existence check
    queue = deque([start])
    visited = {start}

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            return True

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if (
                0 <= new_x < cols
                and 0 <= new_y < rows
                and grid[new_y][new_x] != "#"
                and (new_x, new_y) not in visited
            ):
                queue.append((new_x, new_y))
                visited.add((new_x, new_y))

    return False


def find_blocking_coordinate(coordinates, max_size=71):
    grid = [["."] * max_size for _ in range(max_size)]

    # Process coordinates one by one
    for i, (x, y) in enumerate(coordinates):
        # Add the current byte
        grid[y][x] = "#"

        # Check if path still exists
        if not has_path_to_exit(grid):
            return x, y

    return None


def solve_example():
    example_input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,1
6,1""".splitlines()

    coordinates = []
    for line in example_input:
        x, y = map(int, line.strip().split(","))
        coordinates.append((x, y))

    blocking_coord = find_blocking_coordinate(coordinates, max_size=7)
    print(f"Example blocking coordinate: {blocking_coord[0]},{blocking_coord[1]}")


def main():
    # First solve the example
    solve_example()

    # Then solve the actual input
    print("\nSolving actual input...")
    coordinates = parse_input("day18/input.txt")
    blocking_coord = find_blocking_coordinate(coordinates)
    print(f"Solution: {blocking_coord[0]},{blocking_coord[1]}")


if __name__ == "__main__":
    main()
