def read_input(filename="input.txt"):
    """Read the input file and return two separate lists for sorting."""
    left_list = []
    right_list = []

    try:
        with open(filename, "r") as file:
            print("File opened")
            for line in file:
                # Split each line into two numbers
                left, right = map(int, line.split())
                left_list.append(left)
                right_list.append(right)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please create an input file.")
        exit(1)

    return left_list, right_list


def calculate_total_distance(left_list, right_list):
    """Calculate the total distance between sorted pairs of numbers."""
    # Sort both lists independently
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    total_distance = 0

    # Calculate distance for each pair of sorted numbers
    for left, right in zip(left_sorted, right_sorted):
        distance = abs(left - right)
        total_distance += distance

    return total_distance


def main():
    # Read input with a specific file path
    left_list, right_list = read_input("day1/input.txt")

    # Calculate and print result
    result = calculate_total_distance(left_list, right_list)
    print(f"The total distance between the sorted lists is: {result}")


if __name__ == "__main__":
    main()
