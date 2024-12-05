from collections import defaultdict


def read_input(filename="input.txt"):
    """Read and parse the input file into rules and updates."""
    rules = []
    updates = []
    reading_rules = True

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:  # Empty line separates rules from updates
                    reading_rules = False
                    continue

                if reading_rules:
                    before, after = line.split("|")
                    rules.append((int(before), int(after)))
                else:
                    pages = [int(x) for x in line.split(",")]
                    updates.append(pages)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

    return rules, updates


def build_dependencies(rules):
    """Build a graph of dependencies where key must come before all values in its set."""
    must_come_before = defaultdict(set)
    must_come_after = defaultdict(set)

    for before, after in rules:
        must_come_before[before].add(after)
        must_come_after[after].add(before)

    return must_come_before, must_come_after


def is_valid_order(pages, must_come_before, must_come_after):
    """Check if the pages are in valid order according to the rules."""
    # For each page, check if it violates any rules with pages that come after it
    for i, page in enumerate(pages):
        # Get all pages that should come after this one
        must_follow = must_come_before[page]
        # Get all pages that should come before this one
        must_precede = must_come_after[page]

        # Check pages that come after this one in the sequence
        following_pages = set(pages[i + 1 :])

        # If any page that must come after is not in the following pages
        # and is in the current update, the order is invalid
        for required_follower in must_follow:
            if required_follower in pages and required_follower not in following_pages:
                return False

        # If any page that must come before is in the following pages,
        # the order is invalid
        for required_predecessor in must_precede:
            if required_predecessor in following_pages:
                return False

    return True


def get_middle_page(pages):
    """Get the middle page number from a list of pages."""
    return pages[len(pages) // 2]


def main():
    # Read input
    rules, updates = read_input("day5/input.txt")

    # Build dependency graphs
    must_come_before, must_come_after = build_dependencies(rules)

    # Process each update
    total = 0
    for update in updates:
        if is_valid_order(update, must_come_before, must_come_after):
            middle = get_middle_page(update)
            total += middle

    # Print only the final sum
    print(total)


if __name__ == "__main__":
    main()
