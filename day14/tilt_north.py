import sys

# We have a massive input, maybe doing iteration over every value isn't the
# greatest idea

if (len(sys.argv) != 2):
    sys.exit('Usage: python tilt_north.py input.txt')

# read the grid in from the input file.
with open(sys.argv[1]) as input_file:
    raw_input = input_file.readlines()

input_grid = []
for line in raw_input:
    line = line[:-1]
    print(list(line))
    input_grid.append(list(line))
input_grid = input_grid[:-1]

# might as well tilt every rock up column by column, track
# current position of the last '#' we saw, then shift every
# 'O' up as far as possible.
# have a dict running as well to increment count of rocks
# at each level = len(grid) - i where i is the current
# height we're checking for


def tilt_north(grid):
    num_rocks_at_height = {}
    for i in range(len(grid)):
        num_rocks_at_height[len(grid) - i] = 0
    # initiated the dict
    # loop over the grid and adjust the dict per col
    # len(grid[0]) gets the columns to loop over
    for j in range(len(grid[0])):
        curr_cube = -1
        highest_possible_spot = curr_cube + 1
        # k is the height of a given column
        for k in range(len(grid)):
            if grid[k][j] == '#':
                curr_cube = k
                highest_possible_spot = curr_cube + 1
            elif grid[k][j] == 'O':
                grid[highest_possible_spot][j] = 'O'
                if k != highest_possible_spot:
                    grid[k][j] = '.'
                num_rocks_at_height[len(grid) - highest_possible_spot] += 1
                highest_possible_spot += 1

    print(num_rocks_at_height)
    for line in grid:
        print(line)

    total = 0
    for key in num_rocks_at_height:
        total += key * num_rocks_at_height[key]

    print(total)


tilt_north(input_grid)
