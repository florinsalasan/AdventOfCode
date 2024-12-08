'''
    OK so for this one my idea is to run back the first part, then loop through
    tiles confirmed to be in the guard's path placing a block in each one and
    testing whether it causes a loop, if it does add increment counter
'''

import sys

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 pt1.py puzzle_input')
with open(sys.argv[1]) as open_file:
    lines = open_file.readlines()

listed_lines = []
for line in lines:
    line = listed_lines.append(list(line))

# haven't cleaned up newline characters so need to sub 1 on WIDTH
WIDTH = len(lines[0])
HEIGHT = len(lines)

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
    # print(line)
    for x_idx, value in enumerate(line):
        if x_idx in vertical_movement:
            vertical_movement[x_idx].append(value)
        else:
            vertical_movement[x_idx] = [value]

        if value == '^':
            guard_position["x"] = x_idx
            guard_position["y"] = y_idx

# print('\n ========= \n')

INITIAL_X = guard_position["x"]
INITIAL_Y = guard_position["y"]

# for key in sorted(vertical_movement.keys()):
    # print(vertical_movement[key])


def explore(guard_position, start_direction):
    tiles_covered = set()
    curr_direction = start_direction
    while (guard_position["x"] > 0 and
           guard_position["y"] > 0 and
           guard_position["x"] < WIDTH - 1 and
           guard_position["y"] < HEIGHT - 1):

        if curr_direction == NORTH:
            # go into the vertical_movement dict, at x, and decrement the y
            # to move upwards
            next_position = (vertical_movement[guard_position["x"]]
                             [guard_position["y"] - 1])
        elif curr_direction == SOUTH:
            # go into the vertical_movement dict, at x, and increment the y
            # to move downwards
            next_position = (vertical_movement[guard_position["x"]]
                             [guard_position["y"] + 1])
        elif curr_direction == WEST:
            next_position = lines[guard_position["y"]][guard_position["x"] - 1]
        elif curr_direction == EAST:
            next_position = lines[guard_position["y"]][guard_position["x"] + 1]

        if next_position == '#':
            curr_direction = (curr_direction + 1) % 4
        else:
            tiles_covered.add((guard_position["x"], guard_position["y"]))
            move(curr_direction)

    # This counts the last tille
    tiles_covered.add((guard_position["x"], guard_position["y"]))
    return tiles_covered


possible_obstruction_locations = explore(guard_position, curr_direction)
possible_obstruction_locations.remove((INITIAL_X, INITIAL_Y))


def find_blockages(start_direction):
    curr_direction = start_direction
    counted = 0
    for location in list(possible_obstruction_locations):
        # Start by adding an obstruction in the given location
        x, y = location
        vertical_movement[x][y] = '#'
        listed_lines[y][x] = '#'

        tiles_found = set()
        path_for_second_guard_to_follow = []
        move_trailing_guard = False

        trailing_guard = {"x": INITIAL_X, "y": INITIAL_Y}
        curr_follow_position = 0

        looped = False
        while (guard_position["x"] > 0 and
               guard_position["y"] > 0 and
               guard_position["x"] < WIDTH - 1 and
               guard_position["y"] < HEIGHT - 1) and not looped:

            if curr_direction == NORTH:
                # go into the vertical_movement dict, at x, and decrement the y
                # to move upwards
                next_position = (vertical_movement[guard_position["x"]]
                                 [guard_position["y"] - 1])
            elif curr_direction == SOUTH:
                # go into the vertical_movement dict, at x, and increment the y
                # to move downwards
                next_position = (vertical_movement[guard_position["x"]]
                                 [guard_position["y"] + 1])
            elif curr_direction == WEST:
                next_position = lines[guard_position["y"]][guard_position["x"] - 1]
            elif curr_direction == EAST:
                next_position = lines[guard_position["y"]][guard_position["x"] + 1]

            if next_position == '#':
                curr_direction = (curr_direction + 1) % 4
"""
WHEN CHECKING IF INTERSECTING OR LOOPING, USE THE DIRECTION TO DETERMINE IF IN 
AN ACTUAL LOOP VS JUST CROSSING, DOESN'T HELP NOW SINCE I'M UNDERCOUNTING 
ANYWAYS BUT THIS SHOULD WORK
"""

            else:
                tiles_found.add((guard_position["x"], guard_position["y"]))
                path_for_second_guard_to_follow.append((guard_position["x"], guard_position["y"]))
                if move_trailing_guard:
                    trailing_guard["x"] = path_for_second_guard_to_follow[curr_follow_position][0]
                    trailing_guard["y"] = path_for_second_guard_to_follow[curr_follow_position][1]
                    curr_follow_position += 1
                    if trailing_guard["x"] == guard_position["x"] and trailing_guard["y"] == guard_position["y"]:
                        print("Trailing: ", trailing_guard, " Guard: ", guard_position)
                        looped = True
                    move_trailing_guard = False
                else:
                    move_trailing_guard = True
                move(curr_direction)

        if looped:
            counted += 1

        print("Looped: ", looped)

        # End by removing the obstruction before looping again
        # Reset guard_position
        vertical_movement[x][y] = '.'
        listed_lines[y][x] = '.'
        guard_position["x"] = INITIAL_X
        guard_position["y"] = INITIAL_Y

    print("Valid blockages: ", counted)


find_blockages(curr_direction)
