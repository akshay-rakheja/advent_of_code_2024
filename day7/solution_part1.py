from itertools import product


def read_input(filename="input.txt"):
    """Read and parse the input file into equations."""
    equations = []
    try:
        with open(filename, "r") as file:
            for line in file:
                # Split into test value and numbers
                test_part, nums_part = line.strip().split(": ")
                test_value = int(test_part)
                numbers = [int(x) for x in nums_part.split()]
                equations.append((test_value, numbers))
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
    return equations


def evaluate_expression(numbers, operators):
    """Evaluate expression with given numbers and operators left-to-right."""
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == "+":
            result += numbers[i + 1]
        else:  # op == "*"
            result *= numbers[i + 1]
    return result


def can_equation_be_satisfied(test_value, numbers):
    """Check if equation can be satisfied with any combination of operators."""
    # Number of operators needed is one less than number of numbers
    num_operators = len(numbers) - 1

    # Try all possible combinations of + and *
    for ops in product(["+", "*"], repeat=num_operators):
        if evaluate_expression(numbers, ops) == test_value:
            return True

    return False


def calculate_total_calibration(equations):
    """Calculate sum of test values for satisfiable equations."""
    total = 0
    for test_value, numbers in equations:
        if can_equation_be_satisfied(test_value, numbers):
            total += test_value
    return total


def main():
    # Read input
    equations = read_input("day7/input.txt")

    # Calculate and print result
    result = calculate_total_calibration(equations)
    print(result)


if __name__ == "__main__":
    main()
