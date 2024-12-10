def read_input(filename="input.txt"):
    """Read the disk map from input file."""
    try:
        with open(f"day9/{filename}", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)


def parse_disk_map(disk_map):
    """Parse disk map into list of (length, is_file) tuples."""
    return [(int(char), i % 2 == 0) for i, char in enumerate(disk_map)]


def create_block_representation(sections):
    """Create block representation where each block shows file ID or '.'."""
    total_length = sum(length for length, _ in sections)
    blocks = ["."] * total_length

    pos = 0
    file_id = 0
    file_info = {}  # Store file info while creating blocks

    for length, is_file in sections:
        if is_file:
            file_info[file_id] = (pos, length)  # Store position and length
            for i in range(length):
                blocks[pos + i] = file_id
            file_id += 1
        pos += length

    return blocks, file_info


def find_best_space(blocks, start, required_length):
    """Find the leftmost continuous space that can fit the required length."""
    current_length = 0
    best_start = None

    for i in range(start):
        if blocks[i] == ".":
            if current_length == 0:
                best_start = i
            current_length += 1
            if current_length >= required_length:
                return best_start
        else:
            current_length = 0
            best_start = None

    return None


def compact_files_optimized(blocks, file_info):
    """Optimized version of compacting files by moving whole files."""
    # Process files in decreasing ID order
    for file_id in range(len(file_info) - 1, -1, -1):
        start_pos, length = file_info[file_id]

        # Find best space for this file
        new_pos = find_best_space(blocks, start_pos, length)

        if new_pos is not None:
            # Move the entire file at once using slicing
            blocks[new_pos : new_pos + length] = [file_id] * length
            blocks[start_pos : start_pos + length] = ["."] * length

    return blocks


def calculate_checksum(blocks):
    """Calculate checksum by multiplying position by file ID."""
    checksum = 0
    for pos, block_id in enumerate(blocks):
        if block_id != ".":
            checksum += pos * block_id
    return checksum


def main():
    # Process input
    print("Processing input...")
    disk_map = read_input("input.txt")
    print(f"Input disk map length: {len(disk_map)}")

    sections = parse_disk_map(disk_map)
    blocks, file_info = create_block_representation(sections)
    print(f"Total blocks: {len(blocks)}")
    print(f"Total files: {len(file_info)}")

    # Compact files and calculate checksum
    final_blocks = compact_files_optimized(blocks, file_info)
    checksum = calculate_checksum(final_blocks)
    print(f"\nFinal checksum: {checksum}")


if __name__ == "__main__":
    main()
