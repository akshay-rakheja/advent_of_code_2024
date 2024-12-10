from collections import deque


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
    sections = []
    is_file = True  # Start with file (alternates between file and space)

    # Pre-allocate the list with known size
    sections = [(int(char), i % 2 == 0) for i, char in enumerate(disk_map)]
    return sections


def create_block_representation(sections):
    """Create block representation where each block shows file ID or '.'."""
    # Calculate total length first
    total_length = sum(length for length, _ in sections)
    blocks = ["."] * total_length

    # Fill in file blocks
    pos = 0
    file_id = 0
    for length, is_file in sections:
        if is_file:
            for i in range(length):
                blocks[pos + i] = file_id
            file_id += 1
        pos += length

    return blocks


def compact_files_optimized(blocks):
    """Optimized version of compact_files using two pointers approach."""
    # Convert to list for direct indexing
    blocks = list(blocks)
    total_len = len(blocks)

    # Find initial positions
    left = 0  # Points to first free space
    right = total_len - 1  # Points to last file block

    while left < right:
        # Find next free space from left
        while left < total_len and blocks[left] != ".":
            left += 1
        if left >= right:
            break

        # Find next file block from right
        while right > left and blocks[right] == ".":
            right -= 1
        if right <= left:
            break

        # Swap blocks
        blocks[left], blocks[right] = blocks[right], blocks[left]

    return blocks


def calculate_checksum(blocks):
    """Calculate checksum by multiplying position by file ID."""
    return sum(pos * block_id for pos, block_id in enumerate(blocks) if block_id != ".")


def main():
    # Process actual input directly
    print("Processing input...")
    disk_map = read_input("input.txt")
    print(f"Input disk map length: {len(disk_map)}")

    sections = parse_disk_map(disk_map)
    blocks = create_block_representation(sections)
    print(f"Total blocks: {len(blocks)}")

    # Compact files and calculate checksum
    final_blocks = compact_files_optimized(blocks)
    checksum = calculate_checksum(final_blocks)
    print(f"\nFinal checksum: {checksum}")


if __name__ == "__main__":
    main()
