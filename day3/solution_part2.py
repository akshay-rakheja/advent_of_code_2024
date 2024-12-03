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
    """Find all valid mul instructions and control instructions in the corrupted memory."""
    # Find all mul instructions and their positions
    mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    mul_matches = [
        (match.start(), match.groups()) for match in re.finditer(mul_pattern, memory)
    ]

    # Find all do() and don't() instructions and their positions
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"

    do_positions = [match.start() for match in re.finditer(do_pattern, memory)]
    dont_positions = [match.start() for match in re.finditer(dont_pattern, memory)]

    # Combine control instructions with their type
    controls = [(pos, True) for pos in do_positions] + [
        (pos, False) for pos in dont_positions
    ]
    controls.sort()  # Sort by position

    # Start with multiplications enabled
    enabled = True
    results = []

    # Process each multiplication based on the most recent control instruction
    for mul_pos, (x, y) in mul_matches:
        # Update enabled status based on any control instructions before this multiplication
        while controls and controls[0][0] < mul_pos:
            _, enabled = controls.pop(0)

        # If multiplications are enabled, calculate and store the result
        if enabled:
            result = int(x) * int(y)
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
