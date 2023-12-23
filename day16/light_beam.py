import sys

if (len(sys.argv) != 2):
    sys.exit('Usage: python light_beam.py input.txt')

with open(sys.argv[1]) as input_file:
    lines = input_file.readlines()

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
count = 0


def get_next_node(curr_node, curr_direction, maze):
    # starting the traversal begins with get_next_node([0, 0], 'R', lines)
    # need to find an end condition, probably when the curr_node is out of bounds
    # should be able to call multiple instances of this since it will be recursive
    # all will modify the seen dict, hopefully do not need to deal with
    # loops in the maze.
    x, y = curr_node[0], curr_node[1]
    if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT):
        # out of bounds so return from here, unsure what to return at this moment.
        return
    curr_node_symbol = maze[y][x]
    if (x, y) not in seen:
        seen[(x, y)] = True
        count += 1

    # deal with the different conditions of the light beam direction hitting
    # various symbols.

    # start with direction 'L'
    if curr_direction == 'L':
        if curr_node_symbol == '|':

            # should never not return one of the two possible nodes
    print('Something went wrong, check helper')
    return -1
