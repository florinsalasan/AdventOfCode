import sys

if len(sys.argv) != 2:
    sys.exit('Usage: python dig_plan.py input.txt')

with open(sys.argv[1]) as input_file:
    lines = input_file.readlines()

if lines[-1] == '' or lines[-1] == '\n':
    lines = lines[:-1]


max_up = 0
max_down = 0
curr_up_down = 0
max_left = 0
max_right = 0
curr_left_right = 0


def move_up(count, curr_up_down):
    curr_up_down -= count
    return curr_up_down


def move_down(count, curr_up_down):
    curr_up_down += count
    return curr_up_down


def move_left(count, curr_left_right):
    curr_left_right -= count
    return curr_left_right


def move_right(count, curr_left_right):
    curr_left_right += count
    return curr_left_right


def draw_up(count, curr_up_down):
    new_curr = curr_up_down - count
    return new_curr


def draw_down(count, curr_up_down):
    new_curr = curr_up_down + count
    return new_curr


def draw_left(count, curr_left_right):
    new_curr = curr_left_right - count
    return new_curr


def draw_right(count, curr_left_right):
    new_curr = curr_left_right + count
    return new_curr


def get_block_idxs(grid, y_idx):
    # check if a block has a line leading out from the top and bottom of
    # it otherwise it is an end block and should not be counted towards
    # entering blocks in the main function. is_edge is false iff the
    # lines connecting to blocks are both above and below, if they are
    # only above or only below it must be an edge.

    # Absolutely brutal spaghetti code, apologies to future me and
    # any other person reading this.
    gridline = grid[y_idx]
    # edge for real checks if on the first or last row which will always
    # be an edge
    edge_for_real = False
    if y_idx == 0 or y_idx == len(grid) - 1:
        edge_for_real = True
    blocks = []
    curr_start = 0
    while curr_start < len(gridline):
        # is_edge checks for edges on rows in the middle of the grid
        is_edge = False
        if gridline[curr_start] == '#':
            curr_end = curr_start
            while curr_end + 1 < len(gridline) and gridline[curr_end + 1] == '#':
                curr_end += 1
            if not edge_for_real and curr_start != curr_end:
                if y_idx - 1 >= 0 and grid[y_idx - 1][curr_start] == '#' and grid[y_idx - 1][curr_end] == '#':
                    is_edge = True
                elif y_idx + 1 < len(grid) and grid[y_idx + 1][curr_start] == '#' and grid[y_idx + 1][curr_end] == '#':
                    is_edge = True
                else:
                    is_edge = False

            either_or = is_edge or edge_for_real
            blocks.append((curr_start, curr_end, either_or))
            curr_start += curr_end - curr_start + 1
        else:
            curr_start += 1

    return blocks


for line in lines:
    dir, count, colour = line.split(' ')
    count = int(count)
    dir = dir.lower()
    if dir == 'u':
        new_curr = move_up(count, curr_up_down)
        curr_up_down = new_curr
        if curr_up_down < max_up:
            max_up = curr_up_down

    elif dir == 'd':
        new_curr = move_down(count, curr_up_down)
        curr_up_down = new_curr
        if curr_up_down > max_down:
            max_down = curr_up_down

    elif dir == 'r':
        new_curr = move_right(count, curr_left_right)
        curr_left_right = new_curr
        if curr_left_right > max_right:
            max_right = curr_left_right

    elif dir == 'l':
        new_curr = move_left(count, curr_left_right)
        curr_left_right = new_curr
        if curr_left_right < max_left:
            max_left = curr_left_right


WIDTH = abs(max_right - max_left) + 1
HEIGHT = abs(max_down - max_up) + 1


# create the grid, and a path like we've done before, then count enclosed
# spaces like we've also done before

# If you start the path at -max_left, -max_right, should all fit in a grid
# of WIDTH, HEIGHT as defined above.


grid = []
for i in range(HEIGHT):
    grid.append(list('.' * WIDTH))

curr_left_right = -max_left
curr_up_down = -max_up

for list_item in grid:
    print(list_item)

for line in lines:
    dir, count, colour = line.split(' ')
    count = int(count)
    dir = dir.lower()

    if dir == 'u':
        new_curr = draw_up(count, curr_up_down)
        while curr_up_down != new_curr:
            grid[curr_up_down][curr_left_right] = '#'
            curr_up_down -= 1

    elif dir == 'd':
        new_curr = draw_down(count, curr_up_down)
        while curr_up_down != new_curr:
            grid[curr_up_down][curr_left_right] = '#'
            curr_up_down += 1

    elif dir == 'r':
        new_curr = draw_right(count, curr_left_right)
        while curr_left_right != new_curr:
            grid[curr_up_down][curr_left_right] = '#'
            curr_left_right += 1

    elif dir == 'l':
        new_curr = draw_left(count, curr_left_right)
        while curr_left_right != new_curr:
            grid[curr_up_down][curr_left_right] = '#'
            curr_left_right -= 1

    for item in grid:
        print(item)
    print('\n')

# Outline of the trench should be made in the grid at this point. Need to
# dig out the interior now, by that i mean just get the distance between
# '#' in each line other than the top and bottom which should be a straight
# line. In this approach I'm making a big assumption that it's not like day10
# where the grid can be very complex and 'fold' multiple times on the edges.
# This is very likely a stupidly naive approach that will back fire but I want
# to try for at least part1 anyways.

count = 0

# yeah naive approach did not work, puzzle input is more complex than
# the test input as expected.

# check if a point is enclosed in the trench with counting the num of
# times an index have passed a block of '#'. If it is odd, it is inside
# of the trench, if it is even it is outside the trench.

# wrote the grid to a file so i can visualize the issues better, since
# the console output is cut off in my text editor.

#    stringy_grid = []
#    for item in grid:
#        stringy_grid.append(''.join(item))
#
#    with open('/Users/florinsalasan/VSC_Projects/advent2023/day18/grid.txt', 'w') as fp:
#        fp.write('\n'.join(stringy_grid))

# Generate the dug up count here
for line_idx, line in enumerate(grid):
    block_count = 0
    inside_edges = 0
    blocks = get_block_idxs(grid, line_idx)
    print(blocks)
    if len(blocks) == 1:
        count += blocks[0][1] - blocks[0][0] + 1
    else:
        block_idx = 0
        while block_idx < len(blocks):
            # have the info regarding whether or not the block is an edge
            # or not, need to count in different ways depending on each.
            block = blocks[block_idx]
            start, end, is_edge = block
            if is_edge and block_count % 2 != 1:
                # This block is an edge on the outside and the dug up
                # amount is end - start + 1
                count += end - start + 1
                block_idx += 1
            elif is_edge:
                inside_edges += end - start + 1
                count += end - start + 1
                block_idx += 1
            else:
                # everything from start to the next non edge block end
                # is dug up and inside_edges is subtracted to avoid
                # double counting those blocks
                check_idx = block_idx + 1
                while check_idx < len(blocks) and blocks[check_idx][-1]:
                    check_idx += 1
                # found next non edge to close this section
                # subtract 1 from check_idx since we increment it
                # one too many times in the above while loop
                if check_idx < len(blocks):
                    last_value = blocks[check_idx][1]
                    print(last_value, start, inside_edges)
                    count += last_value - start + 1 - inside_edges
                inside_edges = 0
                block_idx = check_idx

    print(count)
print(count)

print(HEIGHT * WIDTH)
