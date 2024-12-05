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
    for i, page in enumerate(pages):
        following_pages = set(pages[i + 1 :])

        # Check if any required followers are missing from the following pages
        for required_follower in must_come_before[page]:
            if required_follower in pages and required_follower not in following_pages:
                return False

        # Check if any required predecessors appear after this page
        for required_predecessor in must_come_after[page]:
            if required_predecessor in following_pages:
                return False

    return True


def topological_sort(pages, must_come_before, must_come_after):
    """Sort pages according to the dependency rules."""
    # Create a copy of the dependencies for the pages we have
    local_before = defaultdict(set)
    local_after = defaultdict(set)

    # Only include rules relevant to our pages
    page_set = set(pages)
    for page in pages:
        for follower in must_come_before[page]:
            if follower in page_set:
                local_before[page].add(follower)
        for predecessor in must_come_after[page]:
            if predecessor in page_set:
                local_after[page].add(predecessor)

    # Sort pages based on dependencies
    result = []
    remaining = set(pages)

    while remaining:
        # Find a page with no remaining predecessors
        for page in remaining:
            if not any(page in local_after[other] for other in remaining):
                result.append(page)
                remaining.remove(page)
                break

    return result


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
        if not is_valid_order(update, must_come_before, must_come_after):
            # Sort the invalid update
            sorted_update = topological_sort(update, must_come_before, must_come_after)
            middle = get_middle_page(sorted_update)
            total += middle

    # Print only the final sum
    print(total)


if __name__ == "__main__":
    main()
