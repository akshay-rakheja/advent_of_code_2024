def read_input(filename="input.txt"):
    """Read the input file and return list of level reports."""
    reports = []

    try:
        with open(filename, "r") as file:
            for line in file:
                # Convert each line into a list of integers
                levels = list(map(int, line.split()))
                reports.append(levels)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please create an input file.")
        exit(1)

    return reports


def is_safe_report(levels):
    """Check if a report is safe based on the given rules."""
    if len(levels) < 2:
        return False

    # Check first difference to determine if we should be increasing or decreasing
    first_diff = levels[1] - levels[0]
    if first_diff == 0:  # No change is not allowed
        return False

    expected_direction = first_diff > 0  # True for increasing, False for decreasing

    # Check each adjacent pair
    for i in range(len(levels) - 1):
        diff = levels[i + 1] - levels[i]

        # Check if difference is between 1 and 3 (inclusive)
        if abs(diff) < 1 or abs(diff) > 3:
            return False

        # Check if direction matches throughout
        if expected_direction and diff <= 0:
            return False
        if not expected_direction and diff >= 0:
            return False

    return True


def is_safe_with_dampener(levels):
    """Check if a report is safe, considering the Problem Dampener."""
    # First check if it's safe without removing any level
    if is_safe_report(levels):
        return True

    # Try removing each level one at a time
    for i in range(len(levels)):
        # Create a new list without the current level
        dampened_levels = levels[:i] + levels[i + 1 :]
        if is_safe_report(dampened_levels):
            return True

    return False


def count_safe_reports_with_dampener(reports):
    """Count how many reports are safe with the Problem Dampener."""
    return sum(1 for report in reports if is_safe_with_dampener(report))


def main():
    # Read input with a specific file path
    reports = read_input("day2/input.txt")

    # Calculate and print result
    result = count_safe_reports_with_dampener(reports)
    print(f"Number of safe reports with Problem Dampener: {result}")


if __name__ == "__main__":
    main()
