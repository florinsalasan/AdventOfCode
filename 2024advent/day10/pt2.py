import sys

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 pt1.py puzzle_input.txt')
with open(sys.argv[1]) as open_file:
    read_lines = open_file.readlines()

lines = []
for line in read_lines:
    lines.append(line[:-1])

WIDTH = len(lines[0])
HEIGHT = len(lines)

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (-1, 0)
WEST = (1, 0)

DIRECTIONS = {
        "n": NORTH,
        "e": EAST,
        "s": SOUTH,
        "w": WEST,
}

# always increases by exactly one, always starts at height 0 ends at 9
# so begin by finding the zeros

zeros = []
for y_idx, line in enumerate(lines):
    for x_idx, value in enumerate(line):
        if value == "0":
            zeros.append((x_idx, y_idx))

# Walk along the path, finding all possible trails for each 0
trailscore_sum = 0
for zero in zeros:
    print(zero)


def add_tuples(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])


def find_next_tile(curr_position):
    x, y = curr_position
    curr_value = lines[y][x]
    next_valid_positions = []
    for direction in DIRECTIONS.values():
        next_possible_position = add_tuples(curr_position, direction)
        next_pos_x, next_pos_y = next_possible_position
        if (next_pos_x >= 0 and
                next_pos_x < WIDTH and
                next_pos_y >= 0 and
                next_pos_y < HEIGHT):
            # check if next value is one higher than curr value
            next_value = lines[next_pos_y][next_pos_x]
            if int(next_value) == int(curr_value) + 1:
                next_valid_positions.append(next_possible_position)

    return next_valid_positions


# Want only unique 9s reached for each zero, not just every possible path to
# every single 9, so if there are two different paths that reach the same 9
# that only counts as 1 towards the trailscore_sum
for zero in zeros:
    zero_trailsum = 0
    curr_x, curr_y = zero
    curr_value = int(lines[curr_y][curr_x])
    to_check_trail = find_next_tile((curr_x, curr_y))
    while to_check_trail != []:
        # print(to_check_trail)
        next_to_check = to_check_trail.pop()
        curr_x, curr_y = next_to_check
        curr_value = int(lines[curr_y][curr_x])
        # print("Checking curr_value: ", curr_value, " at x: ", curr_x, " y: ", curr_y)
        if curr_value == 9:
            zero_trailsum += 1
            # print("running score: ", len(zero_trailsum))
            continue
        else:
            to_check_trail += find_next_tile((curr_x, curr_y))
    trailscore_sum += zero_trailsum
    print("final_zero_trailsum: ", zero_trailsum, " zero: ", zero)

print("final score: ", trailscore_sum)
