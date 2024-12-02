def read_input(filename="input.txt"):
    """Read the input file and return two separate lists."""
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


def calculate_similarity_score(left_list, right_list):
    """Calculate similarity score based on frequency matching."""
    # Create frequency map for right list
    right_freq = {}
    for num in right_list:
        right_freq[num] = right_freq.get(num, 0) + 1

    total_score = 0

    # For each number in left list, multiply by its frequency in right list
    for num in left_list:
        # Get frequency (default to 0 if number doesn't exist in right list)
        freq = right_freq.get(num, 0)
        score = num * freq
        total_score += score

    return total_score


def main():
    # Read input with a specific file path
    left_list, right_list = read_input("day1/input.txt")

    # Calculate and print result
    result = calculate_similarity_score(left_list, right_list)
    print(f"The similarity score is: {result}")


if __name__ == "__main__":
    main()
