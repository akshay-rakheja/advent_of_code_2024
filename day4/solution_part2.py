def read_input(filename="input.txt"):
    """Read the input file and return the word search grid."""
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please create an input file.")
        exit(1)


def check_diagonal_pattern(grid, row, col, pattern, down=True, right=True):
    """Check if pattern exists in given diagonal direction."""
    height = len(grid)
    width = len(grid[0])

    # Calculate direction modifiers
    row_dir = 1 if down else -1
    col_dir = 1 if right else -1

    # Check boundaries
    end_row = row + (len(pattern) - 1) * row_dir
    end_col = col + (len(pattern) - 1) * col_dir

    if not (
        0 <= end_row < height
        and 0 <= col < width
        and 0 <= row < height
        and 0 <= end_col < width
    ):
        return False

    # Check each character
    for i in range(len(pattern)):
        curr_row = row + i * row_dir
        curr_col = col + i * col_dir
        if grid[curr_row][curr_col] != pattern[i]:
            return False

    return True


def find_xmas_pattern(grid, row, col):
    """Check if an X-MAS pattern exists starting at this position."""
    # The two possible MAS patterns
    mas_forward = "MAS"
    mas_backward = "SAM"

    # Check all possible combinations of diagonal patterns
    # For downward X
    for pattern1, pattern2 in [
        (mas_forward, mas_forward),
        (mas_forward, mas_backward),
        (mas_backward, mas_forward),
        (mas_backward, mas_backward),
    ]:
        # Check downward X pattern
        if check_diagonal_pattern(
            grid, row, col, pattern1, down=True, right=True
        ) and check_diagonal_pattern(
            grid, row, col + 2, pattern2, down=True, right=False
        ):
            return True

        # Check upward X pattern
        if check_diagonal_pattern(
            grid, row + 2, col, pattern1, down=False, right=True
        ) and check_diagonal_pattern(
            grid, row + 2, col + 2, pattern2, down=False, right=False
        ):
            return True

    return False


def count_xmas_patterns(grid):
    """Count all X-MAS patterns in the grid."""
    height = len(grid)
    width = len(grid[0])
    count = 0

    # Try each possible starting position
    for row in range(height - 2):
        for col in range(width - 2):
            if find_xmas_pattern(grid, row, col):
                count += 1

    return count


def main():
    # Read input with a specific file path
    grid = read_input("day4/input.txt")

    # Count X-MAS patterns
    count = count_xmas_patterns(grid)

    # Print only the count
    print(count)


if __name__ == "__main__":
    main()
