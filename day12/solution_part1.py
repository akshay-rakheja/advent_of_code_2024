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


def calculate_perimeter(garden_map, region):
    """Calculate the perimeter of a region."""
    rows, cols = len(garden_map), len(garden_map[0])
    perimeter = 0
    plant_type = garden_map[list(region)[0][0]][list(region)[0][1]]

    for pos in region:
        r, c = pos
        # Check each side
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_r, new_c = r + dr, c + dc
            # Count edge if it's outside map or different plant type
            if (
                new_r < 0
                or new_r >= rows
                or new_c < 0
                or new_c >= cols
                or garden_map[new_r][new_c] != plant_type
            ):
                perimeter += 1

    return perimeter


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

    for region in regions:
        area = len(region)
        perimeter = calculate_perimeter(garden_map, region)
        price = area * perimeter
        total_price += price

        # Store region info for debugging
        plant_type = garden_map[list(region)[0][0]][list(region)[0][1]]
        region_prices[plant_type].append((area, perimeter, price))

    # Print region details
    print("\nRegion details:")
    for plant_type, regions in sorted(region_prices.items()):
        for i, (area, perimeter, price) in enumerate(regions, 1):
            print(
                f"Region {plant_type}{i}: area={area}, perimeter={perimeter}, price={price}"
            )

    return total_price


def main():
    # Test with example input first
    print("Testing with example input...")
    garden_map = read_input("test_input.txt")
    print(f"Map dimensions: {len(garden_map)}x{len(garden_map[0])}")

    # Calculate total price for test
    total_price = calculate_total_price(garden_map)
    print(f"\nTest total price of fencing: {total_price}")
    print("Expected price: 1930")

    # Now process actual input
    print("\nProcessing actual input...")
    garden_map = read_input("input.txt")
    print(f"Map dimensions: {len(garden_map)}x{len(garden_map[0])}")

    # Calculate total price
    total_price = calculate_total_price(garden_map)
    print(f"\nFinal total price of fencing: {total_price}")


if __name__ == "__main__":
    main()
