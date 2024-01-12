# Looked at David Brownman's writeup of his solution and explanation to
# come up with my solution, was nice to know that Dijkstra's was a good
# path to start on, I just couldn't figure out the constraint of number of
# tiles in a row for a given direction. For the full write up see:
# https://advent-of-code.xavd.id/writeups/2023/day/17/

# Coordinates will be (x, y) accessing value in the input will be
# pruned[y][x] to access properly

from heapq import heappop, heappush
import sys

if len(sys.argv) != 2:
    sys.exit('usage: python crucible.py input.txt')

with open(sys.argv[1]) as input_file:
    lines = input_file.readlines()

pruned = []
if lines[-1] == '\n' or lines[-1] == '':
    lines = lines[:-1]

for line in lines:
    # each line ends in newline character, so remove it
    pruned.append(line[:-1])


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

WIDTH = len(pruned[0])
HEIGHT = len(pruned)


_OFFSETS = {
    UP: (0, -1),
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0)
}


def find_path(grid, max_count):
    # start is (0, 0), end is (WIDTH - 1, HEIGHT - 1)
    end = (WIDTH - 1, HEIGHT - 1)
    queue = [
        # Entries in queue, are the heat cost, the coords along
        # with direction, and finally num_steps taken in the same
        # direction to be able to ensure that we don't go over 3
        (0, ((0, 0), DOWN), 0),
        (0, ((0, 0), RIGHT), 0)
    ]
    seen = set()

    while queue:
        cost, position, steps = heappop(queue)
        if position[0] == end:
            return cost
        if (position, steps) in seen:
            continue
        seen.add((position, steps))

        # cannot turn 180 degrees, so get the 3 possible
        # next steps and then push them into the queue if they
        # are in bounds.
        surrounding = get_next_nodes(position)


def get_next_nodes(curr_node):
    surrounding = {}
    curr_direction = curr_node[-1]
    print(curr_node)

    # CW = clockwise, CCW = counterclockwise
    dir_CW = (curr_direction + 1) % 4
    dir_CCW = (curr_direction - 1) % 4

    curr_x = curr_node[0][0]
    curr_y = curr_node[0][1]

    # Get the offsets and add it to the current coords
    # continuing forwards
    forward_x = _OFFSETS[curr_direction][0] + curr_x
    forward_y = _OFFSETS[curr_direction][1] + curr_y
    surrounding[curr_direction] = ((forward_x, forward_y), curr_direction)

    # turning CW
    cw_x = _OFFSETS[dir_CW][0] + curr_x
    cw_y = _OFFSETS[dir_CW][1] + curr_y
    surrounding[dir_CW] = ((cw_x, cw_y), dir_CW)

    # turning CCW
    ccw_x = _OFFSETS[dir_CCW][0] + curr_x
    ccw_y = _OFFSETS[dir_CCW][1] + curr_y
    surrounding[dir_CCW] = ((ccw_x, ccw_y), dir_CCW)

    print(surrounding)
    return surrounding


find_path(pruned, 3)
