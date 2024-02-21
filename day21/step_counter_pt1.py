import sys

if (len(sys.argv) != 2):
    sys.exit('Usage: python enclosed.py maze.txt')

with open(sys.argv[1]) as maze_file:
    lines = maze_file.readlines()

newline_removed = []
for line in lines:
    newline_removed.append(list(line)[:-1])

# have a proper grid now, look for starting point;
for y_idx, line_ in enumerate(newline_removed):
    if 'S' in line_:
        starting_coord = (line_.index('S'), y_idx)
        break

HEIGHT = len(newline_removed)
WIDTH = len(newline_removed[0])


# Finding the starting coord worked for test
# make a pathing function that takes in the grid, along with the remaining
# steps. need a way to check surrounding tiles if they are not a rock
def walk(garden_grid, starting_coord, steps_remaining):
    if steps_remaining == 0:
        print(starting_coord)
        return starting_coord
    next_steps = viable_paths(garden_grid, starting_coord)
    for step in next_steps:
        walk(garden_grid, step, steps_remaining - 1)


def viable_paths(garden_grid, starting_coord):
    # check if N, S, E, W are available to path to.
    directions = {
        # all coords are x, y
        'N': [0, -1],
        'S': [0, 1],
        'E': [1, 0],
        'W': [-1, 0],
    }
    viable_coords = []
    x, y = starting_coord[0], starting_coord[1]
    for key in directions.keys():
        xd, xy = x + directions[key][0], y + directions[key][1]
        if in_bounds((xd, xy)):
            viable_coords.append((xd, xy))
    return viable_coords


def in_bounds(coord):
    x, y = coord[0], coord[1]
    if x < 0 or y < 0 or x >= WIDTH or y >= HEIGHT:
        return False
    return True


coords = walk(newline_removed, starting_coord, 6)
print('coords: ' + str(coords))
