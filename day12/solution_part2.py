from collections import defaultdict, deque


def read_input(filename="input.txt"):
    """Read the garden map from input file."""
    try:
        with open(f"day12/{filename}", "r") as file:
            return [list(line.strip()) for line in file]
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)


def get_neighbors(pos, rows, cols):
    """Get valid neighboring positions (up, down, left, right)."""
    r, c = pos
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # up, down, left, right
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < rows and 0 <= new_c < cols:
            neighbors.append((new_r, new_c))
    return neighbors


def find_region(garden_map, start_pos, visited):
    """Find all positions in a region starting from start_pos."""
    rows, cols = len(garden_map), len(garden_map[0])
    plant_type = garden_map[start_pos[0]][start_pos[1]]
    region = set()
    queue = deque([start_pos])

    while queue:
        pos = queue.popleft()
        if pos in visited or garden_map[pos[0]][pos[1]] != plant_type:
            continue

        region.add(pos)
        visited.add(pos)

        for next_pos in get_neighbors(pos, rows, cols):
            if (
                next_pos not in visited
                and garden_map[next_pos[0]][next_pos[1]] == plant_type
            ):
                queue.append(next_pos)

    return region


def normalize_side(r, c, dr, dc):
    """Normalize side coordinates to ensure consistent representation.
    A side is always represented by the coordinates of its top/left cell."""
    # For vertical sides (left/right walls)
    if dc != 0:
        # Always use the left cell's coordinates
        return (r, min(c, c + dc), True)
    # For horizontal sides (top/bottom walls)
    else:
        # Always use the top cell's coordinates
        return (min(r, r + dr), c, False)


def get_all_neighbors(garden_map, r, c):
    """Get all neighboring cells and their types."""
    rows, cols = len(garden_map), len(garden_map[0])
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < rows and 0 <= new_c < cols:
            neighbors.append((new_r, new_c, garden_map[new_r][new_c]))
    return neighbors


def get_sharing_regions(garden_map, r, c, dr, dc, debug=False):
    """Get all regions that share a side at the given position."""
    rows, cols = len(garden_map), len(garden_map[0])
    sharing_types = set()

    if debug:
        print(f"\nAnalyzing shared regions at ({r}, {c}) direction ({dr}, {dc})")

    # Get the current region's type
    current_type = garden_map[r][c]
    sharing_types.add(current_type)

    # Get the adjacent cell's type (if it exists)
    new_r, new_c = r + dr, c + dc
    if 0 <= new_r < rows and 0 <= new_c < cols:
        adjacent_type = garden_map[new_r][new_c]
        if adjacent_type != current_type:
            sharing_types.add(adjacent_type)

    # For vertical sides, check cells above and below
    if dc != 0:
        for check_r in [r - 1, r, r + 1]:
            if 0 <= check_r < rows:
                # Check both sides of the boundary
                left_c = min(c, c + dc)
                right_c = max(c, c + dc)
                if 0 <= left_c < cols and 0 <= right_c < cols:
                    left_type = garden_map[check_r][left_c]
                    right_type = garden_map[check_r][right_c]
                    if left_type != right_type:
                        sharing_types.add(left_type)
                        sharing_types.add(right_type)
                        if debug:
                            print(f"  Row {check_r}: {left_type} | {right_type}")

    # For horizontal sides, check cells to the left and right
    else:
        for check_c in [c - 1, c, c + 1]:
            if 0 <= check_c < cols:
                # Check both sides of the boundary
                top_r = min(r, r + dr)
                bottom_r = max(r, r + dr)
                if 0 <= top_r < rows and 0 <= bottom_r < rows:
                    top_type = garden_map[top_r][check_c]
                    bottom_type = garden_map[bottom_r][check_c]
                    if top_type != bottom_type:
                        sharing_types.add(top_type)
                        sharing_types.add(bottom_type)
                        if debug:
                            print(f"  Col {check_c}: {top_type} | {bottom_type}")

    if debug:
        print(f"  Sharing types: {sorted(sharing_types)}")

    return sharing_types


def count_sides(garden_map, region, debug=False):
    """Count the number of distinct sides in a region."""
    rows, cols = len(garden_map), len(garden_map[0])
    plant_type = garden_map[list(region)[0][0]][list(region)[0][1]]

    if debug:
        print(f"\n{'='*40}")
        print(f"Analyzing region of type {plant_type} with {len(region)} cells")
        print("Region cells:", sorted(region))

        # Print region boundaries
        min_r = min(r for r, _ in region)
        max_r = max(r for r, _ in region)
        min_c = min(c for _, c in region)
        max_c = max(c for _, c in region)
        print(f"Region boundaries: rows [{min_r}, {max_r}], cols [{min_c}, {max_c}]")

        # Print region shape
        print("\nRegion shape:")
        for r in range(min_r, max_r + 1):
            row = ""
            for c in range(min_c, max_c + 1):
                if (r, c) in region:
                    row += plant_type
                else:
                    row += "."
            print(row)

    # Track each cell's exposed sides with normalized coordinates
    sides = set()

    # For each cell in the region
    for r, c in sorted(region):  # Sort for consistent debug output
        if debug:
            print(f"\nChecking cell ({r}, {c})")

        # Check each direction
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # up, down, left, right
            new_r, new_c = r + dr, c + dc

            # If outside map or different plant type, this is a side
            if (
                new_r < 0
                or new_r >= rows
                or new_c < 0
                or new_c >= cols
                or garden_map[new_r][new_c] != plant_type
            ):

                # Normalize the side coordinates
                side = normalize_side(r, c, dr, dc)

                # Check if this side is already counted
                if side not in sides:
                    # For shared sides between regions, only count if:
                    # 1. It's an outside edge, or
                    # 2. The current region has the lowest type among all adjacent regions
                    should_count = True
                    if 0 <= new_r < rows and 0 <= new_c < cols:
                        # Get all regions that share this side
                        sharing_types = get_sharing_regions(
                            garden_map, r, c, dr, dc, debug
                        )

                        # Only count if this region has the lowest type among all sharing regions
                        # or if it's a corner case where we need to count both sides
                        if len(sharing_types) > 2:  # Corner case with multiple regions
                            # Count if we're the lowest type or if we're adjacent to the lowest type
                            min_type = min(sharing_types)
                            other_types = [t for t in sharing_types if t != plant_type]
                            should_count = (
                                plant_type == min_type
                                or (
                                    len(other_types) > 0
                                    and min(other_types) > plant_type
                                )
                                or any(
                                    t != plant_type
                                    and t == min_type
                                    and sum(1 for x in sharing_types if x == t) > 1
                                    for t in sharing_types
                                )
                            )
                        else:
                            # For simple shared sides, count if we're the lowest type
                            # or if we're equal to the other type and it's a corner
                            other_type = next(
                                t for t in sharing_types if t != plant_type
                            )
                            should_count = plant_type < other_type or (
                                plant_type == other_type
                                and any(
                                    garden_map[r + dr][c + dc] != plant_type
                                    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                                    if 0 <= r + dr < rows and 0 <= c + dc < cols
                                )
                            )

                        if debug:
                            print(f"  Side sharing analysis:")
                            print(f"    Current type: {plant_type}")
                            print(f"    Sharing types: {sorted(sharing_types)}")
                            print(f"    Should count: {should_count}")

                    if should_count:
                        sides.add(side)
                        if debug:
                            print(f"  Added side {side}")
                            print(f"  Current side count: {len(sides)}")

    if debug:
        print("\nFinal sides for region {plant_type}:")
        horizontal_sides = sorted(s for s in sides if s[2])
        vertical_sides = sorted(s for s in sides if not s[2])
        print("  Horizontal sides:")
        for side in horizontal_sides:
            print(f"    {side}")
        print("  Vertical sides:")
        for side in vertical_sides:
            print(f"    {side}")
        print(
            f"Total sides: {len(sides)} ({len(horizontal_sides)} horizontal, {len(vertical_sides)} vertical)"
        )
        print("=" * 40 + "\n")

    return len(sides)


def find_all_regions(garden_map):
    """Find all regions in the garden map."""
    rows, cols = len(garden_map), len(garden_map[0])
    visited = set()
    regions = []

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                region = find_region(garden_map, (r, c), visited)
                regions.append(region)

    return regions


def calculate_total_price(garden_map):
    """Calculate the total price of fencing all regions."""
    regions = find_all_regions(garden_map)
    total_price = 0
    region_prices = defaultdict(list)  # For debugging

    # First, analyze the test case regions in detail
    if len(garden_map) == 10:  # This is the test case
        print("\nDetailed analysis of test case regions:")
        for i, region in enumerate(regions, 1):
            plant_type = garden_map[list(region)[0][0]][list(region)[0][1]]
            area = len(region)
            print(f"\n=== Region {plant_type}{i} ===")
            print(f"Area: {area} cells")
            sides = count_sides(garden_map, region, debug=True)
            price = area * sides
            print(f"Price calculation: {area} cells × {sides} sides = {price}")
            region_prices[plant_type].append((area, sides, price))
            total_price += price
            print(f"Running total: {total_price}")
    else:
        # For the actual input, just process without detailed logging
        for region in regions:
            area = len(region)
            sides = count_sides(garden_map, region)
            price = area * sides
            plant_type = garden_map[list(region)[0][0]][list(region)[0][1]]
            region_prices[plant_type].append((area, sides, price))
            total_price += price

    # Print region details
    print("\nRegion details:")
    for plant_type, regions in sorted(region_prices.items()):
        for i, (area, sides, price) in enumerate(regions, 1):
            print(f"Region {plant_type}{i}: area={area}, sides={sides}, price={price}")

    return total_price


def get_region_sides(garden_map, region, debug=False):
    """Get all sides of a region, including shared ones."""
    rows, cols = len(garden_map), len(garden_map[0])
    sides = set()
    plant_type = garden_map[list(region)[0][0]][list(region)[0][1]]

    # For each cell in the region
    for r, c in region:
        # Check each direction
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_r, new_c = r + dr, c + dc

            # If outside map or different plant type, this is a side
            if (
                new_r < 0
                or new_r >= rows
                or new_c < 0
                or new_c >= cols
                or garden_map[new_r][new_c] != plant_type
            ):

                # Normalize the side coordinates
                side = normalize_side(r, c, dr, dc)
                sides.add(side)

    return sides


def get_adjacent_regions(garden_map, region):
    """Get all regions adjacent to the given region."""
    rows, cols = len(garden_map), len(garden_map[0])
    plant_type = garden_map[list(region)[0][0]][list(region)[0][1]]
    adjacent = set()

    # For each cell in the region
    for r, c in region:
        # Check each direction
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_r, new_c = r + dr, c + dc

            # If inside map and different plant type
            if (
                0 <= new_r < rows
                and 0 <= new_c < cols
                and garden_map[new_r][new_c] != plant_type
            ):
                adjacent.add(garden_map[new_r][new_c])

    return adjacent


def solve(garden_map, debug=False):
    """Solve the garden fencing problem."""
    rows, cols = len(garden_map), len(garden_map[0])
    total_sides = 0

    # First, identify all regions
    regions = {}  # type -> set of (r, c)
    for r in range(rows):
        for c in range(cols):
            plant_type = garden_map[r][c]
            if plant_type not in regions:
                regions[plant_type] = set()
            regions[plant_type].add((r, c))

    # Sort regions by type
    sorted_types = sorted(regions.keys())

    # For each region type
    for plant_type in sorted_types:
        if debug:
            print(f"\nProcessing region type {plant_type}")

        region = regions[plant_type]
        sides = get_region_sides(garden_map, region, debug)
        adjacent = get_adjacent_regions(garden_map, region)

        # Count sides based on adjacency rules
        for side in sides:
            # Always count sides that are on the map boundary
            r, c, is_horizontal = side
            if (
                r < 0
                or r >= rows
                or c < 0
                or c >= cols
                or (is_horizontal and (r == 0 or r == rows))
                or (not is_horizontal and (c == 0 or c == cols))
            ):
                total_sides += 1
                if debug:
                    print(f"  Counting boundary side {side}")
                continue

            # For shared sides, count if we're the lowest type among adjacent regions
            should_count = True
            for adj_type in adjacent:
                if adj_type < plant_type:
                    should_count = False
                    break

            if should_count:
                total_sides += 1
                if debug:
                    print(f"  Counting shared side {side}")

    return total_sides


def main():
    # Test with example input first
    print("Testing with example input...")
    garden_map = read_input("test_input.txt")
    print(f"Map dimensions: {len(garden_map)}x{len(garden_map[0])}")

    # Calculate total price for test
    total_price = calculate_total_price(garden_map)
    print(f"\nTest total price of fencing: {total_price}")
    print("Expected price: 1206")

    # Now process actual input
    print("\nProcessing actual input...")
    garden_map = read_input("input.txt")
    print(f"Map dimensions: {len(garden_map)}x{len(garden_map[0])}")

    # Calculate total price
    total_price = calculate_total_price(garden_map)
    print(f"\nFinal total price of fencing: {total_price}")


if __name__ == "__main__":
    main()
