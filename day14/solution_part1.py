# Same contents as before, just renamed from part1.py to solution_part1.py


def parse_input(file_path):
    robots = []
    with open(file_path, "r") as f:
        for line in f:
            # Parse position and velocity
            pos, vel = line.strip().split(" ")
            px, py = map(int, pos[2:].split(","))
            vx, vy = map(int, vel[2:].split(","))
            robots.append(((px, py), (vx, vy)))
    return robots


def simulate_step(robots, width, height):
    new_positions = []
    for (px, py), (vx, vy) in robots:
        # Update position
        new_x = (px + vx) % width
        new_y = (py + vy) % height
        new_positions.append(((new_x, new_y), (vx, vy)))
    return new_positions


def count_robots_in_quadrants(robots, width, height):
    # Initialize quadrant counts
    quadrants = [0] * 4
    mid_x = width // 2
    mid_y = height // 2

    for (x, y), _ in robots:
        # Skip robots on the middle lines
        if x == mid_x or y == mid_y:
            continue

        # Determine quadrant (0: top-left, 1: top-right, 2: bottom-left, 3: bottom-right)
        quadrant = (2 if y > mid_y else 0) + (1 if x > mid_x else 0)
        quadrants[quadrant] += 1

    return quadrants


def solve(input_file):
    robots = parse_input(input_file)
    width, height = 101, 103

    # Simulate 100 seconds
    for _ in range(100):
        robots = simulate_step(robots, width, height)

    # Count robots in each quadrant
    quadrants = count_robots_in_quadrants(robots, width, height)

    # Calculate safety factor (multiply all quadrant counts)
    safety_factor = 1
    for count in quadrants:
        safety_factor *= count

    return safety_factor


if __name__ == "__main__":
    result = solve("day14/input.txt")
    print(f"Safety factor after 100 seconds: {result}")
