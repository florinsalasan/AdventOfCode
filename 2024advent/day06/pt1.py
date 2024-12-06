import sys

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 pt1.py puzzle_input')
with open(sys.argv[1]) as open_file:
    lines = open_file.readlines()

# haven't cleaned up newline characters so need to sub 1 on WIDTH
WIDTH = len(lines[0])
HEIGHT = len(lines)

print(WIDTH)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

curr_direction = NORTH

# Collect the vertical lists at all x_idxs, should help things speed up a bit,
# Maybe easier edge detection this way too
vertical_movement = {}
guard_position = {"x": 0, "y": 0}


def move_north():
    guard_position["y"] -= 1


def move_south():
    guard_position["y"] += 1


def move_east():
    guard_position["x"] += 1


def move_west():
    guard_position["x"] -= 1


def move(direction):
    if direction == 0:
        move_north()
    elif direction == 1:
        move_east()
    elif direction == 2:
        move_south()
    elif direction == 3:
        move_west()


for y_idx, line in enumerate(lines):
    line = list(line)[:-1]
    print(line)
    for x_idx, value in enumerate(line):
        if x_idx in vertical_movement:
            vertical_movement[x_idx].append(value)
        else:
            vertical_movement[x_idx] = [value]

        if value == '^':
            guard_position["x"] = x_idx
            guard_position["y"] = y_idx

print('\n ========= \n')

for key in sorted(vertical_movement.keys()):
    print(vertical_movement[key])

print("initial guard_position: ", guard_position)
covered = 0
tiles_covered = set()
while (guard_position["x"] > 0 and
       guard_position["y"] > 0 and
       guard_position["x"] < WIDTH - 1 and
       guard_position["y"] < HEIGHT - 1):

    if curr_direction == NORTH:
        # go into the vertical_movement dict, at x_idx, and decrement the y_idx
        # to move upwards
        next_position = (vertical_movement[guard_position["x"]]
                         [guard_position["y"] - 1])
    elif curr_direction == SOUTH:
        # go into the vertical_movement dict, at x_idx, and increment the y_idx
        # to move downwards
        next_position = (vertical_movement[guard_position["x"]]
                         [guard_position["y"] + 1])
    elif curr_direction == WEST:
        next_position = lines[guard_position["y"]][guard_position["x"] - 1]
    elif curr_direction == EAST:
        next_position = lines[guard_position["y"]][guard_position["x"] + 1]

    if next_position == '#':
        print("curr_direction before update: ", curr_direction)
        curr_direction = (curr_direction + 1) % 4
        print(curr_direction)
    else:
        print(guard_position["x"], guard_position["y"])
        tiles_covered.add((guard_position["x"], guard_position["y"]))
        move(curr_direction)

print(tiles_covered)
# I don't count the final tile where it exits the area so add 1
print(len(tiles_covered) + 1)
