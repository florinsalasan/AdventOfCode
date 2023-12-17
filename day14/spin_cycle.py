import sys

if (len(sys.argv) != 3):
    sys.exit('Usage: python tilt_north.py input.txt NUM_CYCLES')

NUM_CYCLES = int(sys.argv[2])

# read the grid in from the input file.
with open(sys.argv[1]) as input_file:
    raw_input = input_file.readlines()

input_grid = []
for line in raw_input:
    line = line[:-1]
    print(list(line))
    input_grid.append(line)
input_grid = input_grid[:-1]
print(input_grid)

# How do i reduce 1 billion iterations of the spin cycle
# for a grid that is 100 lines tall. I think the play is
# break it down line by line and column by column then
# have 4 dicts, key being the current state, value being
# the value after tilting the rocks every way. Biggest
# issue would be reconstructing the grid after every
# call to tilt N, W, S, E. Once we've done 1 billion
# iterations of this, get the total load on northern
# support beams.

tilt_line_dict = {}

# modify tilt north function from part1 to create a vertical
# line and then use a helper that checks the dict for a cached
# value. rebuild the grid and return the modified version
# can have the tilt line function be used for every version
# then just have functions that rotate the grid every time.

# once the vertical lines all exist, 'rotate' by recreating the grid
# from last to first, then tilt everything north again. This
# results in effectively going N - W, W - S, S - E, E - N


def rotate_grid(grid):
    print(grid)
    verts = [[]for x in range((len(grid[0])))]
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            verts[col].append(grid[row][col])
    str_verts = []
    for vert in verts:
        append_this = ''.join(vert)
        str_verts.append(append_this)
    to_return = []
    for i in range(len(str_verts) - 1, -1, -1):
        # for i in range(len(grid)):
        to_return.append(str_verts[i])

    print('rotated, og')
    print(str_verts, grid)

    return str_verts


def tilt(grid):
    new_grid = []
    for line in grid:
        curr_line = list(line)
        new_grid.append(tilt_line(curr_line))

    return new_grid


def tilt_line(line):
    curr_line = ''.join(line)
    if curr_line in tilt_line_dict:
        return tilt_line_dict[line]
    else:
        curr_line = line
        curr_cube = -1
        highest_possible_spot = curr_cube + 1
        for k in range(len(curr_line)):
            if line[k] == '#':
                curr_cube = k
                highest_possible_spot = curr_cube + 1
            elif line[k] == 'O':
                curr_line[highest_possible_spot] = 'O'
                if k != highest_possible_spot:
                    curr_line[k] = '.'
                highest_possible_spot += 1
        to_return = ''.join(curr_line)
        return to_return

# Ok so have a function that tilts every line, then returns
# the tilted grid, then we can rotate the grid to then call tilt
# on the new grid again. repeat 4 times for a cycle, NUM_CYCLES
# for the number of cycles


curr_grid = input_grid
for i in range(NUM_CYCLES * 4):
    # tilt it,
    curr_grid = tilt(curr_grid)
    # rotate it,
    curr_grid = rotate_grid(curr_grid)

    if (i - 1) % 4 == 0:
        print('east:')
    elif (i - 1) % 3 == 0:
        print('south:')
    elif (i - 1) % 2 == 0:
        print('west:')
    else:
        print('north:')

    for line in curr_grid:
        print(line)

    print('')


# count 'O' on each line to calc load on north beams
curr_grid = rotate_grid(curr_grid)
for line in curr_grid:
    print(line)
