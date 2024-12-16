def parse_input(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Parse the map
    map_lines = []
    i = 0
    while lines[i].strip() != "":
        map_lines.append(lines[i].strip())
        i += 1

    # Skip empty line
    i += 1

    # Parse movement sequence
    moves = ""
    while i < len(lines):
        moves += lines[i].strip()
        i += 1

    return map_lines, moves


def find_robot_position(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "@":
                return (x, y)
    return None


def try_move(grid, robot_pos, direction, move_char):
    width = len(grid[0])
    height = len(grid)
    x, y = robot_pos
    dx, dy = direction

    print(f"\nAttempting move {move_char} from position ({x}, {y})")

    # Calculate new position
    new_x = x + dx
    new_y = y + dy

    # Check if hitting wall
    if grid[new_y][new_x] == "#":
        print(f"Hit wall at ({new_x}, {new_y}), no movement")
        return grid, robot_pos

    # Check if pushing box(es)
    if grid[new_y][new_x] == "O":
        # Find all boxes that would be pushed in a chain
        boxes_to_push = []
        check_x, check_y = new_x, new_y

        # Keep looking ahead until we find something that's not a box
        while True:
            if grid[check_y][check_x] == "O":
                boxes_to_push.append((check_x, check_y))
                check_x += dx
                check_y += dy
            else:
                break

        # Check if the chain of boxes can be pushed (needs empty space at the end)
        if grid[check_y][check_x] != ".":
            print(
                f"Cannot push boxes - blocked by {grid[check_y][check_x]} at ({check_x}, {check_y})"
            )
            return grid, robot_pos

        # Move is valid, update grid
        new_grid = [list(row) for row in grid]

        # First clear all positions
        new_grid[y][x] = "."  # Clear robot's old position
        for box_x, box_y in boxes_to_push:
            new_grid[box_y][box_x] = "."  # Clear each box's old position

        # Then place all boxes in their new positions (one space forward)
        for box_x, box_y in boxes_to_push:
            new_box_x = box_x + dx
            new_box_y = box_y + dy
            new_grid[new_box_y][new_box_x] = "O"  # Place box in new position
            print(f"Pushed box from ({box_x}, {box_y}) to ({new_box_x}, {new_box_y})")

        # Place robot in the first box's old position
        new_grid[new_y][new_x] = "@"
        print(f"Robot moved to ({new_x}, {new_y})")
        return ["".join(row) for row in new_grid], (new_x, new_y)

    # Simple move without pushing
    new_grid = [list(row) for row in grid]
    new_grid[y][x] = "."
    new_grid[new_y][new_x] = "@"
    print(f"Simple move to ({new_x}, {new_y})")
    return ["".join(row) for row in new_grid], (new_x, new_y)


def calculate_gps_coordinates(grid):
    total = 0
    print("\nCalculating GPS coordinates:")
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                # Count from edges of map (including walls)
                # For a box at array position (x,y):
                # Distance from top = y (count: edge→wall→position)
                # Distance from left = x (count: edge→wall→position)
                gps = 100 * y + x
                print(
                    f"Box at ({x}, {y}) -> distance from top: {y}, from left: {x}, GPS: {gps}"
                )
                total += gps
    return total


def solve(input_file, test_mode=False):
    if test_mode:
        # Use the example from the problem
        grid = [
            "########",
            "#..O.O.#",
            "##@.O..#",
            "#...O..#",
            "#.#.O..#",
            "#...O..#",
            "#......#",
            "########",
        ]
        moves = "<^^>>>vv<v>>v<<"
        print("Using test input with expected sum: 2028")
    else:
        grid, moves = parse_input(input_file)

    robot_pos = find_robot_position(grid)
    print(f"\nInitial robot position: {robot_pos}")

    # Direction mappings
    directions = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}

    # Debug: Print initial state
    print("\nInitial state:")
    for row in grid:
        print(row)

    # Process each move
    for move in moves:
        if move in directions:
            grid, robot_pos = try_move(grid, robot_pos, directions[move], move)
            print("\nCurrent state:")
            for row in grid:
                print(row)

    # Debug: Print final state
    print("\nFinal state:")
    for row in grid:
        print(row)

    # Calculate final GPS coordinates
    result = calculate_gps_coordinates(grid)
    if test_mode:
        print(f"\nTest result: {result} (Expected: 2028)")
        if result == 2028:
            print("✓ Test passed!")
        else:
            print("✗ Test failed!")
    return result


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run with test input")
    args = parser.parse_args()

    result = solve("day15/input.txt", test_mode=args.test)
    print(f"\nSum of GPS coordinates: {result}")


if __name__ == "__main__":
    main()
