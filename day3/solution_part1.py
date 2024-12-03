import re


def read_input(filename="input.txt"):
    """Read the input file and return the corrupted memory string."""
    try:
        with open(filename, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please create an input file.")
        exit(1)


def find_valid_multiplications(memory):
    """Find all valid mul instructions in the corrupted memory."""
    # Pattern for valid mul instruction: exactly 'mul' followed by parentheses
    # containing 1-3 digits, comma, 1-3 digits
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"

    # Find all matches
    matches = re.finditer(pattern, memory)

    results = []
    for match in matches:
        x, y = map(int, match.groups())
        result = x * y
        results.append(result)

    return results


def calculate_total(results):
    """Calculate the sum of all multiplication results."""
    return sum(results)


def main():
    # Read input with a specific file path
    memory = read_input("day3/input.txt")

    # Find all valid multiplications and their results
    results = find_valid_multiplications(memory)

    # Calculate and print only the total
    total = calculate_total(results)
    print(total)


if __name__ == "__main__":
    main()
