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
global count
count = 0


def get_next_node(curr_node, curr_direction, maze):
    # starting the traversal begins with get_next_node([0, 0], 'R', lines)
    # need to find an end condition, probably when the curr_node is out of bounds
    # should be able to call multiple instances of this since it will be recursive
    # all will modify the seen dict, hopefully do not need to deal with
    # loops in the maze.
    global count
    x, y = curr_node[0], curr_node[1]
    print(x, y)
    # need to write better base cases so that the function will actually return
    # at some point
    if count > WIDTH * HEIGHT:
        return 0
    if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT):
        # out of bounds so return from here, unsure what to return at this moment.
        return 0
    curr_node_symbol = maze[y][x]
    if (x, y) in seen:
        if curr_direction in seen[(x, y)]:
            return 0
        else:
            seen[(x, y)] += [curr_direction]
    if (x, y) not in seen:
        seen[(x, y)] = [curr_direction]

    # deal with the different conditions of the light beam direction hitting
    # various symbols.

    # prepare all of 4 possible next nodes
    node_above = (curr_node[0] + directions['U'][0],
                  curr_node[1] + directions['U'][1])
    node_below = (curr_node[0] + directions['D'][0],
                  curr_node[1] + directions['D'][1])
    node_left = (curr_node[0] + directions['L'][0],
                 curr_node[1] + directions['L'][1])
    node_right = (curr_node[0] + directions['R'][0],
                  curr_node[1] + directions['R'][1])

    # start with direction 'L'
    if curr_direction == 'L':
        if curr_node_symbol == '|':
            return 1 + get_next_node(node_above, 'U', maze) + get_next_node(node_below, 'D', maze)
        elif curr_node_symbol == "\\":
            return 1 + get_next_node(node_above, 'U', maze)
        elif curr_node_symbol == '/':
            return 1 + get_next_node(node_below, 'D', maze)
        else:
            return 1 + get_next_node(node_left, 'L', maze)

    elif curr_direction == 'R':
        if curr_node_symbol == '|':
            return 1 + get_next_node(node_above, 'U', maze) + get_next_node(node_below, 'D', maze)
        elif curr_node_symbol == "\\":
            return 1 + get_next_node(node_below, 'D', maze)
        elif curr_node_symbol == '/':
            return 1 + get_next_node(node_above, 'U', maze)
        else:
            return 1 + get_next_node(node_right, 'R', maze)

    elif curr_direction == 'U':
        if curr_node_symbol == '-':
            return 1 + get_next_node(node_right, 'R', maze) + get_next_node(node_left, 'L', maze)
        elif curr_node_symbol == "\\":
            return 1 + get_next_node(node_left, 'L', maze)
        elif curr_node_symbol == '/':
            return 1 + get_next_node(node_right, 'R', maze)
        else:
            return 1 + get_next_node(node_above, 'U', maze)

    elif curr_direction == 'D':
        if curr_node_symbol == '-':
            return 1 + get_next_node(node_right, 'R', maze) + get_next_node(node_left, 'L', maze)
        elif curr_node_symbol == "\\":
            return 1 + get_next_node(node_right, 'R', maze)
        elif curr_node_symbol == '/':
            return 1 + get_next_node(node_left, 'L', maze)
        else:
            return 1 + get_next_node(node_below, 'D', maze)

            # should never not return one of the two possible nodes
    print('Something went wrong, check helper')
    return -1


print(get_next_node((0, 0), 'R', lines))
print(len(seen.keys()))
print(seen)
