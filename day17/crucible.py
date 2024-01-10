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


def find_path(grid, start=(0, 0, '')):
    # Generate all nodes and put them inside of an unvisited
    # nodes list, along with initiating the distance to infinity
    unvisited_nodes = []

    shortest_paths = {}

    previous_nodes = {}

    for x in range(WIDTH):
        for y in range(HEIGHT):
            curr_node = (x, y)
            unvisited_nodes.append(curr_node)
            shortest_paths[curr_node] = float('inf')

    # initialize the start node to have a dist of 0
    shortest_paths[(0, 0)] = 0
    while unvisited_nodes:
        # Get the node with the smallest value, first iteration
        # will be the start node with a value of 0
        curr_min_node = None
        for node in unvisited_nodes:
            if curr_min_node is None:
                curr_min_node = node
            elif shortest_paths[node] < shortest_paths[curr_min_node]:
                curr_min_node = node

        # have the node with the smallest value, get the surrounding nodes
        neighbours = get_surrounding_nodes(curr_min_node)
        for neighbour in neighbours:
            x = neighbour[0]
            y = neighbour[1]
            # this sum is the value of the distance so far plus the value
            # of a neighbour coord which acts as the weighted edge
            test_value = shortest_paths[curr_min_node] + \
                int(grid[y][x])
            if test_value < shortest_paths[(x, y)]:
                shortest_paths[(x, y)] = test_value
                # set a value for previous_nodes
                previous_nodes[(x, y)] = curr_min_node

        unvisited_nodes.remove(curr_min_node)

    return previous_nodes, shortest_paths


def get_surrounding_nodes(curr_coords):
    # given an object that has x, y in first two indices,
    # return the nodes that are connected and ensure that
    # the nodes are in bounds.
    possible_nodes = []
    to_return = []
    for direction in DIRECTIONS.keys():
        possible_nodes.append(
            (curr_coords[0] + DIRECTIONS[direction][0], curr_coords[1] + DIRECTIONS[direction][1], direction))
    for potential in possible_nodes:
        x = potential[0]
        y = potential[1]
        if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
            to_return.append(potential)

    return to_return


print(find_path(lines))
