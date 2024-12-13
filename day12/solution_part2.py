from collections import deque
from typing import Set, Tuple, List, Dict


def read_input(filename: str) -> List[str]:
    with open(filename, "r") as f:
        return [line.strip() for line in f]


def find_regions(grid: List[str]) -> Dict[str, List[Set[Tuple[int, int]]]]:
    rows, cols = len(grid), len(grid[0])
    visited = set()
    regions = {}  # type -> list of regions

    def get_neighbors(r: int, c: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        return neighbors

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r][c] != ".":
                current_type = grid[r][c]
                region = set()
                queue = deque([(r, c)])

                while queue:
                    curr_r, curr_c = queue.popleft()
                    if (curr_r, curr_c) in visited:
                        continue

                    visited.add((curr_r, curr_c))
                    region.add((curr_r, curr_c))

                    for nr, nc in get_neighbors(curr_r, curr_c):
                        if (nr, nc) not in visited and grid[nr][nc] == current_type:
                            queue.append((nr, nc))

                if current_type not in regions:
                    regions[current_type] = []
                regions[current_type].append(region)

    return regions


def count_sides(region: Set[Tuple[int, int]], grid: List[str]) -> int:
    rows, cols = len(grid), len(grid[0])
    sides = 0

    # Helper to check if a position is part of the region
    def is_region(r: int, c: int) -> bool:
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        return (r, c) in region

    # Check each cell in the region
    for r, c in region:
        # Check all four directions
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # If neighbor is not part of region, this cell contributes to a side
            if not is_region(nr, nc):
                sides += 1

    # Each side is counted twice (once from each cell), so divide by 2
    return sides // 2


def calculate_price(grid: List[str]) -> int:
    regions = find_regions(grid)
    total_price = 0

    # Process each type's regions
    for plant_type, type_regions in regions.items():
        for region in type_regions:
            area = len(region)
            sides = count_sides(region, grid)
            price = area * sides
            total_price += price
            print(
                f"Region of type {plant_type}: Area={area}, Sides={sides}, Price={price}"
            )

    return total_price


def main():
    grid = read_input("day12/input.txt")
    price = calculate_price(grid)
    print(f"\nTotal price: {price}")


if __name__ == "__main__":
    main()
