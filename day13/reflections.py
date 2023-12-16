import sys
import math


if (len(sys.argv)) != 2:
    sys.exit('Usage: python reflections.py input.txt')

grids = []
# Should I make a dict for each possible coordinate in a grid?
# might make it faster since there will be a lot of looping
# when creating the vertical lines to check for reflections.
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


def find_reflection(grid):
    # given a grid look for any reflection
    # horizontally first, then if none found
    # look for them vertically.

    # DO NOT LOOK THROUGH EVERY POSSIBLE COMBO
    # ONLY NEED TO LOOK AND FIND WHICH LINE MATCHES
    # ONE OF THE EDGES this might still be worse
    # than checking every pair if they're equal
    # but in my heart it seems faster plan is start
    # at idx 0 for rows, check against max_row every time
    # loop through until an identical row has been found or
    # reach the end of the rows, then do the same for vertical
    # lines. worst case for this is the two lines being identical
    # are the last two vertical lines in the grid.
    # what if the reflection is closer to the start so the
    # final column/row does not have a reflection?
    # take the following input:
    #
    # ..##.......
    # ..##.......
    # ..##.......
    # ..##.......
    # ..##.......
    #
    # this breaks my algo in very many ways,
    # first because the way it currently works it would think
    # that the first and last columns are the reflection so
    # it would assume that the line of reflection would be
    # in the middle rather than between cols 2 and 3 (0 indexed)
    # I guess a fix would be testing if the proposed middle is also
    # equal to one another, but then in the case above, that still
    # wouldn't fix anything, since the middle is just two lines of
    # dots, iterating over the grid and checking if every pair is equal
    # to find the middle wouldn't work in this case because it would think
    # that the first two are the reflection point, and would be unable
    # to determine if it's a valid line since there are no other lines to
    # the left of the start to compare to col at idx 2. Maybe this is just an
    # invalid input and I'm stressing too much for now. But the naive approach
    # of finding a middle and then checking every pair after to ensure that
    # they are all matching seems like the one way to avoid edge cases for now
    # but the run time for that approach seems way over the top.

    max_col = len(grid[0]) - 1
    curr_col = 0
    max_row = len(grid) - 1
    curr_row = 0

    # start with comparing rows
    found = False
    while not found and curr_row < max_row:
        found = compare_two_lines(grid[curr_row], grid[max_row])
        if not found:
            curr_row += 1
        # realistically do not need the check below, but it makes
        # it comfy and easier to read the logic imo
        elif found:
            temp_up_middle = curr_row + math.floor((max_row - curr_row) / 2)
            temp_down_middle = temp_up_middle + 1
            max_len = len(grid) - 1
            # calling all lines between can set found back to false if it is not a real reflection,
            # in order to continue iterating through.
            print(temp_up_middle, temp_down_middle)
            print(curr_row, max_row)
            found = all_lines_between_reflected(
                'horizontal', grid, 0, max_len, temp_down_middle, temp_up_middle)
            if not found:
                curr_row += 1

    if found:
        # reflection is horizontal and then we can use the curr_row
        # and max_row to find the point where the reflection exists
        # by taking the floor of the difference / 2, this is the
        # first row on top so to speak, add one to get the index
        # of the row below
        top_row_idx = curr_row + math.floor((max_row - curr_row) / 2)
        bottom_row_idx = top_row_idx + 1
        return summarize('horizontal', bottom_row_idx)

    # should probably compare rows from the last row iterating up and always
    # comparing to the first row in the grid in case the reflection is nearer
    # to the top. since max row was not equal to the first row, start at max_row
    # - 1, to save one comparison
    while not found and max_row >= 1:
        found = compare_two_lines(grid[0], grid[max_row - 1])
        if not found:
            max_row -= 1
        elif found:
            temp_up_middle = math.floor(max_row / 2)
            temp_down_middle = temp_up_middle + 1
            max_len = len(grid) - 1
            # calling all lines between can set found back to false if it is not a real reflection,
            # in order to continue iterating through.
            found = all_lines_between_reflected(
                'horizontal', grid, 0, max_len, temp_down_middle, temp_up_middle)
            if not found:
                max_row -= 1

    if found:
        # found horizontal reflection from 0th row to whatever max_row - 1 is
        # use the diff to set top and bottom row idxs one of the edges will be
        # 0 so just take the floor of max_row / 2
        top_row_idx = math.floor(max_row / 2)
        bottom_row_idx = top_row_idx + 1
        return summarize('horizontal', bottom_row_idx)

    # didn't find the reflection horizontally, need to check vertically,
    # need to create the vertical line to pass into compare_two_lines,
    # can reuse the line at the end of the grid each time, but
    # need to make new ones each time curr_col moves

    # create the line to use at max_col,
    last_col = create_line(grid, max_col)
    while not found and curr_col < max_col:
        curr_col_line = create_line(grid, curr_col)
        found = compare_two_lines(curr_col_line, last_col)
        if not found:
            curr_col += 1
        elif found:
            temp_up_middle = curr_col + math.floor(max_col - curr_col / 2) + 1
            temp_down_middle = temp_up_middle + 1
            max_len = len(grid[0]) - 1
            # calling all lines between can set found back to false if it is not a real reflection,
            # in order to continue iterating through.
            found = all_lines_between_reflected(
                'vertical', grid, 0, max_len, temp_down_middle, temp_up_middle)
            if not found:
                curr_col += 1
    if found:
        # vertical reflection was found, same method of finding the
        # indices of the reflection as it was for rows, just use the
        # column values instead
        first_col_idx = curr_col + math.floor((max_col - curr_col) / 2)
        second_col_idx = first_col_idx + 1
        return summarize('vertical', second_col_idx)

    # do the same reverse check as we did in the horizontal one if not found.
    first_col = create_line(grid, 0)
    while not found and max_col > 0:
        line_to_comp = create_line(grid, max_col - 1)
        found = compare_two_lines(first_col, line_to_comp)
        if not found:
            max_col -= 1
        elif found:
            temp_up_middle = math.floor(max_col / 2) + 1
            temp_down_middle = temp_up_middle + 1
            max_len = len(grid[0]) - 1
            # calling all lines between can set found back to false if it is not a real reflection,
            # in order to continue iterating through.
            found = all_lines_between_reflected(
                'vertical', grid, 0, max_len, temp_down_middle, temp_up_middle)
            if not found:
                max_col -= 1

    if found:
        # found horizontal reflection from 0th row to whatever max_row - 1 is
        # use the diff to set top and bottom row idxs one of the edges will be
        # 0 so just take the floor of max_row / 2
        left_col = math.floor(max_col / 2) + 1
        return summarize('vertical', left_col)

    # should only ever return 0 if there is no reflection
    return 0


def all_lines_between_reflected(reflection_type, grid, upper_end_idx, low_end_idx, low_middle, upper_middle):
    # given where it reflects, how it reflects and the range to check, ensure
    # all necessary lines are equal to one another
    print(reflection_type, low_middle, upper_middle)
    equal = True
    if reflection_type == 'vertical':
        # my naming is bad but low middle is essentially the one that
        # has a higher index, or shows up later when
        # iterating from 0 to max
        while equal and (upper_middle >= upper_end_idx and low_middle < low_end_idx):
            # have to make a new line for each given line ahh
            # assume first call is made low_end and upper_end excluding the
            # indices that were first used to find the reflection line
            line1 = create_line(grid, upper_middle)
            line2 = create_line(grid, low_middle)
            equal = compare_two_lines(line1, line2)
            if equal:
                upper_middle -= 1
                low_middle += 1

    else:
        while equal and (upper_middle >= upper_end_idx and low_middle < low_end_idx):
            # have to make a new line for each given line ahh
            # assume first call is made low_end and upper_end excluding the
            # indices that were first used to find the reflection line
            print('testing horizontal')
            print(low_middle, upper_middle)
            line1 = grid[upper_middle]
            line2 = grid[low_middle]
            equal = compare_two_lines(line1, line2)
            if equal:
                upper_middle -= 1
                low_middle += 1

    return equal


def summarize(reflection_type, num_before_reflection):
    # returns the modifications to the count of whatever the number
    # of rows and cols are from the reflection
    if reflection_type == 'horizontal':
        return num_before_reflection * 100
    else:
        return num_before_reflection


def create_line(grid, col_idx):
    # assume valid input given, will not check for out of bounds here
    to_return = []
    for i in range(len(grid)):
        to_return.append(grid[i][col_idx])
    return to_return


def compare_two_lines(line1, line2):
    # input all has equal length lines, so will not
    # check for same length, only same values at each idx.
    for i in range(len(line1)):
        if line1[i] != line2[i]:
            return False
    return True


summary_count = 0
for item in grids:
    summary_count += find_reflection(item)

print(summary_count)

# print(all_lines_between_reflected(
#     'horizontal', grids[1], 0, len(grids[1]) - 1, 4, 3))
