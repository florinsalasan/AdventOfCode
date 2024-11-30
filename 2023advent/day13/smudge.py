import sys
import math

if (len(sys.argv)) != 2:
    sys.exit('Usage: python smudge.py input.txt')

grids = []
with open(sys.argv[1]) as open_file:
    curr_grid = []
    curr_line = open_file.readline()
    while curr_line:
        if curr_line == '\n':
            grids.append(curr_grid)
            curr_grid = []
        else:
            curr_line = curr_line[:-1]
            curr_grid.append(curr_line)

        curr_line = open_file.readline()

for grid in grids:
    for line in grid:
        print(line)
    print('')

# Brother I'm lost, my best possible idea is create a dict where key is
# the string of the edges of the first and list rows, then have some
# dynamic programming like solution where I swap the symbol for
# each position and check if it is in the dict or not, should have a
# separate one for vertical and horizontal reflections.
# The initial edges added in should have values of true,
# then for each line check against the dict, only add in lines that
# are false, when cycling through lines check if the line matches an
# edge when flipping each char. values in the key should be true or
# false along with the idx to be able to check lines in between for
# all of them to be reflections along with the num of lines being even

# Should I add the base versions of all lines into the grid?, would
# make it faster to check for reflections, I think. doing this might
# reduce the search space too, since the first time we find a line that
# is already inside the dict, can look for a smudge in one of the two
# lines that would be the reflection if the first doubled line is
# in the second half of the grid range, check the edge for a smudge
# otherwise.

# new thought since this seems way too hard at the moment, rerun part1
# with one change, instead of the check between function being true
# iff they are all the same, return true if there is only one
# character difference between all of the pairs of lines. Likely
# need to do this recursively instead of iteratively.


def find_vertical_reflections(grid):
    start_idx = 0
    end_idx = len(grid[0]) - 1
    curr_idx = 0

    idxs = []

    # start by comparing from top to last col,
    # if they match ensure that all cols in
    # between match, also ensure that num cols
    # in between are even, other wise cannot be a
    # reflection.

    last_col = create_vert(grid, end_idx)
    while curr_idx < end_idx:
        curr_col = create_vert(grid, curr_idx)
        maybe_match = compare_lines(last_col, curr_col)
        if maybe_match < 2:
            # if the two lines are the same, check how many
            # lines are in between, if even then check each
            # pair is the same
            if (end_idx - curr_idx + 1) % 2 == 0:
                # pass in the idxs of the two lines we know,
                # decrement from end_idx, and increment from curr_idx
                # until end - curr < 1
                match = check_in_between('vertical', grid, curr_idx, end_idx)
                if (maybe_match + match == 1):
                    idxs.append(
                        curr_idx + math.floor((end_idx - curr_idx) / 2) + 1)
        curr_idx += 1

    # now do the same but need to always compare to the first col
    first_col = create_vert(grid, 0)
    while curr_idx > start_idx:
        curr_col = create_vert(grid, curr_idx)
        maybe_match = compare_lines(first_col, curr_col)
        if maybe_match < 2:
            # if the two lines are the same, check how many
            # lines are in between, if even then check each
            # pair is the same
            if (curr_idx + 1) % 2 == 0:
                # pass in the idxs of the two lines we know,
                # decrement from end_idx, and increment from curr_idx
                # until end - curr < 1
                match = check_in_between(
                    'vertical', grid, start_idx, curr_idx)
                if (maybe_match + match == 1):
                    idxs.append(math.floor(curr_idx / 2) + 1)
        curr_idx -= 1

    return idxs


def find_horizontal_reflections(grid):
    start_idx = 0
    end_idx = len(grid) - 1
    curr_idx = 0

    idxs = []

    # start by comparing from top to last row,
    # if they match ensure that all rows in
    # between match, also ensure that num rows
    # in between are even, other wise cannot be a
    # reflection.

    while curr_idx < end_idx:
        maybe_match = compare_lines(grid[curr_idx], grid[end_idx])
        if maybe_match < 2:
            # if the two lines are the same, check how many
            # lines are in between, if even then check each
            # pair is the same
            if (end_idx - curr_idx + 1) % 2 == 0:
                # pass in the idxs of the two lines we know,
                # decrement from end_idx, and increment from curr_idx
                # until end - curr < 1
                match = check_in_between('horizontal', grid, curr_idx, end_idx)
                if (maybe_match + match == 1):
                    idxs.append(
                        curr_idx + math.floor((end_idx - curr_idx) / 2) + 1)
        curr_idx += 1

    # now do the same but need to always compare to the first row
    while curr_idx > start_idx:
        maybe_match = compare_lines(grid[curr_idx], grid[start_idx])
        if maybe_match < 2:
            # if the two lines are the same, check how many
            # lines are in between, if even then check each
            # pair is the same
            if (curr_idx + 1) % 2 == 0:
                # pass in the idxs of the two lines we know,
                # decrement from end_idx, and increment from curr_idx
                # until end - curr < 1
                match = check_in_between(
                    'horizontal', grid, start_idx, curr_idx)
                if (maybe_match + match == 1):
                    idxs.append(math.floor(curr_idx / 2) + 1)
        curr_idx -= 1

    return idxs


def compare_lines(line1, line2):
    count_diff = 0
    for i in range(len(line1)):
        if line1[i] != line2[i]:
            count_diff += 1
    return count_diff


def check_in_between(reflection_type, grid, increment_this, decrement_this):
    increment_this += 1
    decrement_this -= 1
    count = 0
    if reflection_type == 'vertical':
        # need to create the vertical lines to compare against each other
        while (decrement_this - increment_this) >= 1:
            line1, line2 = create_verts(grid, increment_this, decrement_this)
            checked_pair = compare_lines(line1, line2)
            return checked_pair + check_in_between('vertical', grid, increment_this, decrement_this)
    else:
        while (decrement_this - increment_this) >= 1:
            line1, line2 = grid[increment_this], grid[decrement_this]
            checked_pair = compare_lines(line1, line2)
            return checked_pair + check_in_between('horizontal', grid, increment_this, decrement_this)

    return count


def create_verts(grid, top_idx, bottom_idx):
    top_line = []
    bottom_line = []
    for i in range(len(grid)):
        top_line.append(grid[i][top_idx])
        bottom_line.append(grid[i][bottom_idx])
    return top_line, bottom_line


def create_vert(grid, idx):
    # only use this version for checking individual
    # lines when looking for vertical reflections
    line = []
    for i in range(len(grid)):
        line.append(grid[i][idx])
    return line

# have the tools to find the proper idxs to summarize everything, just do it
# for each grid now


curr_score = 0
for grid in grids:
    hidxs = find_horizontal_reflections(grid)
    vidxs = find_vertical_reflections(grid)
    for hidx in hidxs:
        curr_score += 100 * hidx
    for vidx in vidxs:
        curr_score += vidx

print(curr_score)
