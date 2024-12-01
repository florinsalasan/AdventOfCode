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


trenched = {}


for line in lines:
    _, __, colour = line.split(' ')

    # dir and count are fake, need to extract that info from colour
    # dir = colour[-3]
    # count = int(colour[2:-2], 16)

    count = int(colour[2:-3], 16)

    dir = colour[-3]
    # direction translation, 0 = r, 1 = d, 2 = l, 3 = u
    if dir == '3':
        new_curr = move_up(count, curr_up_down)
        while curr_up_down > new_curr:
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

    elif dir == '0':
        new_curr = move_right(count, curr_left_right)
        if curr_up_down in trenched:
            trenched[curr_up_down].append(
                (min(curr_left_right, new_curr), max(curr_left_right, new_curr)))
        else:
            trenched[curr_up_down] = [(
                min(curr_left_right, new_curr), max(curr_left_right, new_curr))]

        curr_left_right = new_curr
        if curr_left_right > max_right:
            max_right = curr_left_right

    elif dir == '2':
        new_curr = move_left(count, curr_left_right)
        if curr_up_down in trenched:
            trenched[curr_up_down].append(
                (min(curr_left_right, new_curr), max(curr_left_right, new_curr)))
        else:
            trenched[curr_up_down] = [(
                min(curr_left_right, new_curr), max(curr_left_right, new_curr))]
        curr_left_right = new_curr
        if curr_left_right < max_left:
            max_left = curr_left_right


WIDTH = abs(max_right - max_left) + 1
HEIGHT = abs(max_down - max_up) + 1


def get_block_idxs(x_idxs, y_idx):
    removed_dupes = set()
    actual_x_idxs = []
    for values in x_idxs:
        # This is already the blocks in a tuple, just need to remove
        # duplicates that are equal to an edge for a tuple, also should
        # look above and below to see if it is a an edge or not.
        if type(values) is tuple:
            removed_dupes.add(values[0])
            removed_dupes.add(values[1])
            actual_x_idxs.append(values)
            continue
        # need to add all of the tuples first imo, otherwise could be
        # checking against nothing and adding the duped index when it
        # shouldn't be there.
        if type(values) is not tuple:
            continue
    for values2 in x_idxs:
        if values2 not in removed_dupes:
            if type(values2) is tuple:
                continue
            removed_dupes.add(values2)
            actual_x_idxs.append((values2,))
    # should sort this as well from lowest value to highest
    if len(actual_x_idxs) > 1:
        for i in range(len(actual_x_idxs) - 1):
            for j in range(len(actual_x_idxs) - i - 1):
                if actual_x_idxs[j][0] > actual_x_idxs[j + 1][0]:
                    temp = actual_x_idxs[j]
                    actual_x_idxs[j] = actual_x_idxs[j + 1]
                    actual_x_idxs[j + 1] = temp

    to_return = []

    for block in actual_x_idxs:
        if len(block) == 1:
            to_return.append((block[0], block[0], False))
        else:
            # check if the connections are both above or both below
            if y_idx == max_up or y_idx == max_down:
                to_return.append((block[0], block[1], True))
                continue
            elif (block[0] in trenched[y_idx - 1] and block[1] in trenched[y_idx + 1]) or (block[1] in trenched[y_idx - 1] and block[0] in trenched[y_idx + 1]):
                to_return.append((block[0], block[1], False))
                continue
            else:
                to_return.append((block[0], block[1], True))
                continue

    return to_return

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

    total = 0
    for key in trenched_dict.keys():

        # otherwise need to do the counting ourselves

        blocks = get_block_idxs(trenched[key], key)
        if tuple(blocks) in memoed.keys():
            total += memoed[tuple(blocks)]
            continue

        inside = False
        count = 0
        block_idx = 0
        curr_starting_idx = 0

        while block_idx < len(blocks):
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

        memoed[tuple(blocks)] = count
        total += count

    return total


print(get_dug_up_area(trenched))
