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


def get_block_idxs(gridline, y_idx):
    # check if a block has a line leading out from the top and bottom of
    # it otherwise it is an end block and should not be counted towards
    # entering blocks in the main function. is_edge is false iff the
    # lines connecting to blocks are both above and below, if they are
    # only above or only below it must be an edge.

    # need a way to have the y_idx passed in, it is the key for trenched so
    # should work I think
    print(gridline, y_idx)
    edge_for_real = False
    # check against max up for first row
    if y_idx == max_up or y_idx == HEIGHT - 1:
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


trenched = {}

for line in lines:
    _, __, colour = line.split(' ')

    # dir and count are fake, need to extract that info from colour
    # dir = colour[-3]
    # count = int(colour[2:-2], 16)

    # print(dir, count, colour)
    count = int(colour[2:-3], 16)

    dir = colour[-3]
    # direction translation, 0 = r, 1 = d, 2 = l, 3 = u
    if dir == '3':
        new_curr = move_up(count, curr_up_down)
        while curr_up_down > new_curr:
            print(curr_left_right)
            if curr_up_down in trenched:
                trenched[curr_up_down].append(curr_left_right)
            else:
                trenched[curr_up_down] = [curr_left_right]

            curr_up_down -= 1

        curr_up_down = new_curr
        if curr_up_down < max_up:
            max_up = curr_up_down

    elif dir == '1':
        new_curr = move_down(count, curr_up_down)
        while curr_up_down < new_curr:
            if curr_up_down in trenched:
                trenched[curr_up_down].append(curr_left_right)
            else:
                trenched[curr_up_down] = [curr_left_right]

            curr_up_down += 1

        curr_up_down = new_curr
        if curr_up_down > max_down:
            max_down = curr_up_down

    # TODO: change right and left to add to trenched as well.
    elif dir == '0':
        new_curr = move_right(count, curr_left_right)
        if curr_up_down in trenched:
            trenched[curr_up_down].append(
                (min(curr_left_right, new_curr), max(curr_left_right, new_curr)))
        else:
            trenched[curr_up_down] = (
                min(curr_left_right, new_curr), max(curr_left_right, new_curr))

        curr_left_right = new_curr
        if curr_left_right > max_right:
            max_right = curr_left_right

    elif dir == '2':
        new_curr = move_left(count, curr_left_right)
        if curr_up_down in trenched:
            trenched[curr_up_down].append(
                (min(curr_left_right, new_curr), max(curr_left_right, new_curr)))
        else:
            trenched[curr_up_down] = (
                min(curr_left_right, new_curr), max(curr_left_right, new_curr))
        curr_left_right = new_curr
        if curr_left_right < max_left:
            max_left = curr_left_right

print('finished moving')
print(trenched)

WIDTH = abs(max_right - max_left) + 1
HEIGHT = abs(max_down - max_up) + 1

print(WIDTH, HEIGHT)
print(WIDTH * HEIGHT)

# grid = []
# for i in range(HEIGHT):
# grid.append(list('.' * WIDTH))


# TODO: change the function below to grab from trenched, memoize the
# solution since there's bound to be repeats of lines.
# Can likely either have the whole line as the key, which would likely
# use tons of memory with how large it is or memoized by blocks which
# would likely require large amounts of computation to get the blocks of
# each line first to compare.

def get_dug_up_area(trenched_dict):
    # For any give line in the grid, should be able to determine if we are inside or
    # outside of the trench with a basic ray casting imitation by 'moving' left to
    # right, count non edges to see if we are currently inside or outside of the space
    # start at 0, if non edge increment counting everything inside until new non edge
    # decrement back to 0

    memoed = {}

    for key in trenched_dict.keys():
        if key in memoed.keys():
            return memoed[key]

        # otherwise need to do the counting ourselves

        blocks = get_block_idxs(key, trenched[key])
        inside = False
        count = 0
        block_idx = 0
        curr_starting_idx = 0

        while block_idx < len(blocks):
            print(blocks[block_idx])
            start, end, is_edge = blocks[block_idx]

            if inside and not is_edge:
                # found the end of the current open section of the trench, count
                # the space from curr_starting_idx to end of the block we're on
                count += end - curr_starting_idx + 1
            elif not inside and not is_edge:
                curr_starting_idx = start
            if not is_edge:
                # flip the inside bool here so that both if blocks don't run above.
                inside = not inside
            if is_edge and not inside:
                count += end - start + 1

            block_idx += 1

        return count


print(get_dug_up_area(trenched))
