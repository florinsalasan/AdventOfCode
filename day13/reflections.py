import sys
import math


if (len(sys.argv)) != 2:
    sys.exit('Usage: python reflections.py input.txt')

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


def find_vertical_reflections(grid):
    start_idx = 0
    end_idx = len(grid[0]) - 1
    curr_idx = 0

    idxs = []

    # start by comparing from top to last col,
    # if they match ensure that all cols in
    # between match, also ensure that num rows
    # in between are even, other wise cannot be a
    # reflection.

    # create the last col to reuse
    last_col = create_vert(grid, end_idx)

    while curr_idx < end_idx:
        curr_col = create_vert(grid, curr_idx)
        maybe_match = compare_lines(last_col, curr_col)
        if maybe_match:
            print(curr_idx, end_idx)
            # if the two lines are the same, check how many
            # lines are in between, if even then check each
            # pair is the same
            if (end_idx - curr_idx + 1) % 2 == 0:
                # pass in the idxs of the two lines we know,
                # decrement from end_idx, and increment from curr_idx
                # until end - curr < 1
                match = check_in_between('vertical', grid, curr_idx, end_idx)
                print(match)
                if match[0]:
                    idxs.append(match[1])
        curr_idx += 1

    # now do the same but need to always compare to the first row
    first_col = create_vert(grid, 0)
    while curr_idx > start_idx:
        # should find a way to store the created lists from the
        # first pass to reuse them in this pass when comparing
        # to the first column
        curr_col = create_vert(grid, curr_idx)
        maybe_match = compare_lines(first_col, curr_col)
        if maybe_match:
            print(curr_idx, start_idx)
            # if the two lines are the same, check how many
            # lines are in between, if even then check each
            # pair is the same
            if (curr_idx + 1) % 2 == 0:
                # pass in the idxs of the two lines we know,
                # decrement from end_idx, and increment from curr_idx
                # until end - curr < 1
                match = check_in_between(
                    'vertical', grid, start_idx, curr_idx)
                print(match)
                if match[0]:
                    idxs.append(match[1])
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
        if maybe_match:
            print(curr_idx, end_idx)
            # if the two lines are the same, check how many
            # lines are in between, if even then check each
            # pair is the same
            if (end_idx - curr_idx + 1) % 2 == 0:
                # pass in the idxs of the two lines we know,
                # decrement from end_idx, and increment from curr_idx
                # until end - curr < 1
                match = check_in_between('horizontal', grid, curr_idx, end_idx)
                print(match)
                if match[0]:
                    idxs.append(match[1])
        curr_idx += 1

    # now do the same but need to always compare to the first row
    while curr_idx > start_idx:
        maybe_match = compare_lines(grid[curr_idx], grid[start_idx])
        if maybe_match:
            print(curr_idx, start_idx)
            # if the two lines are the same, check how many
            # lines are in between, if even then check each
            # pair is the same
            if (curr_idx + 1) % 2 == 0:
                # pass in the idxs of the two lines we know,
                # decrement from end_idx, and increment from curr_idx
                # until end - curr < 1
                match = check_in_between(
                    'horizontal', grid, start_idx, curr_idx)
                print(match)
                if match[0]:
                    idxs.append(match[1])
        curr_idx -= 1

    return idxs


def compare_lines(line1, line2):
    for i in range(len(line1)):
        if line1[i] != line2[i]:
            return False
    return True


def check_in_between(reflection_type, grid, increment_this, decrement_this):
    increment_this += 1
    decrement_this -= 1
    if reflection_type == 'vertical':
        # need to create the vertical lines to compare against each other
        while (decrement_this - increment_this) >= 1:
            line1, line2 = create_verts(grid, increment_this, decrement_this)
            checked_pair = compare_lines(line1, line2)
            if not checked_pair:
                print('broken')
                return (False, 0, 0)
            increment_this += 1
            decrement_this -= 1
            print(increment_this, decrement_this)
    else:
        while (decrement_this - increment_this) >= 1:
            line1, line2 = grid[increment_this], grid[decrement_this]
            checked_pair = compare_lines(line1, line2)
            if not checked_pair:
                print('broken')
                return (False, 0, 0)
            increment_this += 1
            decrement_this -= 1
            print(increment_this, decrement_this)

    return (True, increment_this, decrement_this)


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
