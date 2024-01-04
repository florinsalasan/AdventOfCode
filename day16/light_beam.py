import sys

if (len(sys.argv) != 2):
    sys.exit('Usage: python light_beam.py input.txt')

with open(sys.argv[1]) as input_file:
    lines = input_file.readlines()

if lines[-1] == '' or lines[-1] == '\n':
    lines = lines[:-1]

for line in lines:
    print(line)


HEIGHT = len(lines)
WIDTH = len(lines[0])

# light beam enters in the top left corner and moves towards
# the right until it hits some sort of mirror or splitter
# '\' or '/' are mirrors, they change the direction at 90deg angle
# fairly self explanitory. '-' and '|' are the splitters, if the
# beam enters a splitter in the direction the splitter is facing
# it continues as normal, if it hits it in a perpendicular fashion
# then it splits into two and continues in the 2 perpendicular directions
# ie if a beam is coming left to right and hits '|' then it splits up
# and down from the splitting character.

# Probably need a way to walk through the grid, swear there's been a past
# puzzle that had a similar pathing through a grid.
directions = {
    # all directions are x, y
    'L': [-1, 0],
    'R': [1, 0],
    'U': [0, -1],
    'D': [0, 1]
}

# create a dict that contains all of the coordinates of the
# tiles that a lightbeam has passed through
seen = {}

# so my recursive effort was bad, will try doing this iteratively
# don't know how well this will work given that there are splits in the beam

# so the pathing always begins top left corner and continues towards the right
# then the rules with the mirrors and splitters come into effect.


def find_path(maze, start):
    queue = [start]
    # the start position and items in queue should have x, y, then a direction
    # from the dict
    seen = set()  # keep in mind this is unordered, but lets us not have to
    # worry about dupes
    while queue != []:
        curr = queue[0]
        queue = queue[1:]
        curr_direction = directions[curr[-1]]
        new_x = curr[0] + curr_direction[0]
        new_y = curr[1] + curr_direction[1]
        if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
            # means we are inside the grid still so can add it.
            continue

        curr_char = maze[new_y][new_x]

        if (curr_char == '.' or
            (curr_char == '-' and curr_direction[1] != 0) or
                (curr_char == '|' and curr_direction[0] != 0)):
            queue.append((curr[0], curr[1], curr_direction))
            seen.add(curr[0], curr[1], curr_direction)

        # not looking forward to doing all of the different cases
        # for where the path goes next.


find_path(lines, (0, 0, 'R'))
