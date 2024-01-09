import sys

# given a grid of numbers that indicate the amount of heat lost,
# and with a limit of being able to move in the same direction a
# maximum of 3 tiles before needing to turn find the least amount
# of heat loss possible. cannot backtrack, the crucible most
# either move forward, left, or right.

if (len(sys.argv) != 2):
    sys.exit('Usage: python crucible.py input.txt')

with open(sys.argv[1]) as input_file:
    lines = input_file.readlines()

if lines[-1] == '' or lines[-1] == '\n':
    # remove empty line at end of input if needed.
    lines = lines[:-1]

WIDTH = len(lines[0]) - 1  # Lines contain newline character at the end
HEIGHT = len(lines)

# path must start at (0, 0) ends at (WIDTH - 1, HEIGHT - 1)
# heat loss is not incurred at the start unless the path returns to it
# and I cannot think of a reason for the path to ever return that way.

# first potential solution that comes to mind is an implementation
# of Dijkstra's algorithm where the weighted edges are the
# heat loss for each node, and need to have a counter or something
# for how many nodes in a row the crucible has travelled in the same
# direction which should be an interesting wrinkle in the solution.

DIRECTIONS = {'r': [1, 0],
              'l': [-1, 0],
              'd': [0, 1],
              'u': [0, -1]}


def find_path(grid, start=(0, 0, ''), end=(WIDTH - 1, HEIGHT - 1)):
    # I'm going to base this off of the algorithm description from
    # brilliant.org hopefully, this works out since it would be the
    # first time I've implemented dijkstra's

    queue = []
    dists = {}
    seen = set()
    dir = ''
    count_dir = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dists[(x, y)] = float('inf')

    dists[(0, 0)] = 0
    # so starting with start, update the values of the surrounding nodes
    # to their heat loss values + whatever the current value is of the
    # node currently on.

    # get the values of the nodes surrounding the current nodes
    queue.append(start)
    while queue != []:
        # get the coordinates of the curr_node
        x, y, curr_dir = queue.pop(0)
        x = int(x)
        y = int(y)
        if (x, y) in seen:
            continue
        seen.add((x, y))
        curr_dist = dists[(x, y)]
        print(curr_dist)
        surrounding_nodes_coords = []
        valid_coords = []
        for direction in DIRECTIONS.keys():
            surrounding_nodes_coords.append(
                (x + DIRECTIONS[direction][0], y + DIRECTIONS[direction][1], direction))
        for surrounding_coords in surrounding_nodes_coords:
            new_x = surrounding_coords[0]
            new_y = surrounding_coords[1]
            if new_y < 0 or new_y > HEIGHT - 1 or new_x < 0 or new_x > HEIGHT - 1:
                continue
            else:
                if not (new_x, new_y) in seen:
                    valid_coords.append(surrounding_coords)

        # At this point have the coordinates for the surrounding nodes that are within bounds.
        # From here generate the distance of the surrounding nodes by adding the node values in the grid to the
        # curr_node distance value also need to have a way to consider the count_dir if it reaches 3.

        # I think I want to implement the basic version first then add in the constraint
        # of moving at most 3 tiles in the same direction
        for node in valid_coords:
            dists[(node[0], node[1])] = int(grid[node[1]][node[0]]) + curr_dist
            print(node)
            print(dists[(node[0], node[1])])
            queue.append(node)
        valid_coords = []

    print(dists)


find_path(lines)
