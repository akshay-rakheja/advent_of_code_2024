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


def find_shortest_path(grid):
    rows, cols = len(grid), len(grid[0])
    start = (0, 0)
    end = (cols - 1, rows - 1)

    # Priority queue for Dijkstra's algorithm
    # Format: (distance, (x, y))
    pq = [(0, start)]
    visited = set()

    # Possible directions: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while pq:
        dist, (x, y) = heapq.heappop(pq)

        if (x, y) == end:
            return dist

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if (
                0 <= new_x < cols
                and 0 <= new_y < rows
                and grid[new_y][new_x] != "#"
                and (new_x, new_y) not in visited
            ):
                heapq.heappush(pq, (dist + 1, (new_x, new_y)))

    return float("inf")  # No path found


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
5,1""".splitlines()

    coordinates = []
    for line in example_input:
        x, y = map(int, line.strip().split(","))
        coordinates.append((x, y))

    grid = create_grid(coordinates, max_size=7)
    print("Example grid:")
    print_grid(grid)
    steps = find_shortest_path(grid)
    print(f"Example solution: {steps} steps\n")


def main():
    # First solve the example
    solve_example()

    # Then solve the actual input
    print("Solving actual input...")
    coordinates = parse_input("day18/input.txt")
    # Take only first 1024 bytes as specified
    coordinates = coordinates[:1024]
    grid = create_grid(coordinates)
    steps = find_shortest_path(grid)
    print(f"Solution: {steps} steps")


if __name__ == "__main__":
    main()
