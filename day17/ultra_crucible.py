# Continuing from the first part, need to add the minimum number
# of steps in a direction and then rerun the numbers. My problem
# requires min 4 steps, max of 10 steps.

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


def find_path(grid, min_count, max_count):
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
        print(position)
        if position[0] == end and steps >= min_count:
            return cost
        if (position, steps) in seen:
            continue
        seen.add((position, steps))

        # cannot turn 180 degrees, so get the 3 possible
        # next steps and then push them into the queue if they
        # are in bounds.
        surrounding = get_next_nodes(position)
        curr_dir = position[-1]
        for key in surrounding.keys():
            x = surrounding[key][0][0]
            y = surrounding[key][0][1]
            surr_dir = surrounding[key][1]
            if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
                new_cost = int(grid[y][x]) + cost
                if curr_dir == surr_dir:
                    if steps < max_count:
                        heappush(queue,
                                 (new_cost, (surrounding[key][0], surrounding[key][1]), steps + 1))
                else:
                    if steps >= min_count:
                        heappush(
                            queue, (new_cost, (surrounding[key][0], surrounding[key][1]), 1))


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


print(find_path(pruned, 4, 10))
