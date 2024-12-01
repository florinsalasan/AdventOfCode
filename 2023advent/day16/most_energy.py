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

# so the pathing always begins top left corner and continues towards the right
# then the rules with the mirrors and splitters come into effect.


def find_path(maze, start):
    fillable = [list(('.'*(WIDTH - 1))) for x in range(HEIGHT)]
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
        if x < 0 or x >= WIDTH - 1 or y < 0 or y >= HEIGHT:
            # out of bounds, try next value in queue
            continue

        # new_x = x + dx
        # new_y = y + dy

        seen.add((x, y, dx, dy))
        coords.add((x, y))
        fillable[y][x] = '#'

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
    for line in fillable:
        print(line)

    return len(coords)

# for pt2 need to test every possible point of entry along the edges of the grid. for example
# if the starting coordinate is (0, 5) initial direction would be downwards. There's probably
# some way of memoizing this if a given coordinate and direction appears and would have the number
# of tiles energized from there. However given the splitters it might be hard to do this. Will attempt
# brute forcing every entry, if it takes too long might consider the memoized approach.


energized_tiles = []
for i in range(WIDTH):
    # start by going along the top and bottom rows and append the num_energized to above list
    energized_tiles.append(find_path(lines, (i, 0, 0, 1)))
    energized_tiles.append(find_path(lines, (i, HEIGHT - 1, 0, -1)))
for j in range(HEIGHT):
    # finish by going along the left and right columns and append the num_energized to above list
    energized_tiles.append(find_path(lines, (0, j, 1, 0)))
    energized_tiles.append(find_path(lines, (WIDTH - 1, j, -1, 0)))

print(max(energized_tiles))
# This approach worked, took about 1second to run on my machine but it's fast so bad
# point of reference. Would be interesting to revisit this once I complete all 25
# challenges to see if I could come up with a more interesting approach to solving this.
