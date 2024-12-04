def read_input(filename="input.txt"):
    """Read the input file and return the word search grid."""
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please create an input file.")
        exit(1)


def find_word_in_direction(grid, row, col, dx, dy, word):
    """Check if word exists starting at (row,col) in direction (dx,dy)."""
    height = len(grid)
    width = len(grid[0])
    word_len = len(word)

    # Check if the word would fit in this direction
    end_row = row + (word_len - 1) * dy
    end_col = col + (word_len - 1) * dx

    if not (0 <= end_row < height and 0 <= end_col < width):
        return False

    # Check each character of the word
    for i in range(word_len):
        if grid[row + i * dy][col + i * dx] != word[i]:
            return False

    return True


def count_word_occurrences(grid, word):
    """Count all occurrences of word in the grid in all directions."""
    height = len(grid)
    width = len(grid[0])
    count = 0

    # All possible directions
    directions = [
        (0, 1),  # right
        (0, -1),  # left
        (1, 0),  # down
        (-1, 0),  # up
        (1, 1),  # down-right
        (-1, -1),  # up-left
        (1, -1),  # down-left
        (-1, 1),  # up-right
    ]

    # Try each starting position and direction
    for row in range(height):
        for col in range(width):
            for dx, dy in directions:
                if find_word_in_direction(grid, row, col, dx, dy, word):
                    count += 1

    return count


def main():
    # Read input with a specific file path
    grid = read_input("day4/input.txt")

    # Count occurrences of XMAS
    count = count_word_occurrences(grid, "XMAS")

    # Print only the count
    print(count)


if __name__ == "__main__":
    main()
