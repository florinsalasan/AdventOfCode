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
# won't be accessing the directions from the dict, is kinda clunky to do so
# directions = {
# all directions are x, y
#     'L': [-1, 0],
#     'R': [1, 0],
#     'U': [0, -1],
#     'D': [0, 1]
# }

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
    coords = set()
    # worry about dupes
    while queue != []:
        # while the queue is not empty, check the first item
        # and add any other necessary items to the queue
        x, y, dx, dy = queue.pop(0)

        if (x, y, dx, dy) in seen:
            continue

        # check if x, y are valid indices
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            # out of bounds, try next value in queue
            continue

        # new_x = x + dx
        # new_y = y + dy

        seen.add((x, y, dx, dy))
        coords.add((x, y))

        curr_char = maze[y][x]

        if curr_char == '.' or (curr_char == '-' and dy == 0) or (curr_char == '|' and dx == 0):
            # continue in the same direction
            queue.append((x + dx, y + dy, dx, dy))
        # need to expand the conditional since this will double dip if the first conditional goes
        elif curr_char == '-' and dy != 0:
            # splits horizontally left and right, so same y value, x +/- 1 value added to queue
            queue.append((x + 1, y, 1, 0))
            queue.append((x - 1, y, -1, 0))
        elif curr_char == '|' and dx != 0:
            queue.append((x, y + 1, 0, 1))
            queue.append((x, y - 1, 0, -1))
        elif curr_char == '\\':
            # need to check for dy both -1 and 1, and same for dx for
            # all possible next nodes. Unless there is some way to
            # do this more elegantly. The only way I can think of
            # is setting dx to 0 if nonzero, then dy to dx and same
            # for dy if dy is nonzero
            if dy != 0:
                queue.append((x + dy, y, dy, 0))
            elif dx != 0:
                queue.append((x, y + dx, 0, dx))
        elif curr_char == '/':
            # is setting dx to 0 if nonzero, then dy to -dx and same
            # for dy if dy is nonzero
            if dy != 0:
                queue.append((x + (-dy), y, -dy, 0))
            elif dx != 0:
                queue.append((x, y + (-dx), 0, -dx))

        print(curr_char)

    print(coords)


find_path(lines, (0, 0, 1, 0))
