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
    input_grid.append(line)

if input_grid[-1] == '\n' or input_grid[-1] == '':
    input_grid = input_grid[:-1]
stringed_grid = ''.join(input_grid)

for line in input_grid:
    print(line)

print('')

HEIGHT = len(input_grid)
WIDTH = len(input_grid[0])

# New plan, modify one big string doing some
# math tilting in each direction,
# once we reach a state where the tilted grid is
# in the dict, we can do modulo operation to
# find which state to go to in the reverse lookup

tilt_line_dict = {}
reverse_lookup = {}

print(HEIGHT, WIDTH)


def spin_cycle(stringed_grid):
    tilted_north = tilt_north(stringed_grid)
    # print('tilted_north: ' + tilted_north)
    # print('')
    # print_grid(tilted_north)
    # print('')
    tilted_west = tilt_west(tilted_north)
    # print('tilted_west: ' + tilted_west)
    # print('')
    # print_grid(tilted_west)
    # print('')
    tilted_south = tilt_south(tilted_west)
    # print('tilted_south: ' + tilted_south)
    # print('')
    # print_grid(tilted_south)
    # print('')
    tilted_east = tilt_east(tilted_south)
    # print('tilted_east: ' + tilted_east)
    # print('')
    # print_grid(tilted_east)
    # print('')

    tilt_line_dict[stringed_grid] = tilted_east

    return tilted_east


def tilt_north(stringed_grid):
    len_str = len(stringed_grid)
    curr_string = stringed_grid
    for i in range(0, WIDTH, 1):
        # The i loop lets the j - loop create the vertical
        # lines
        highest_possible_idx = i
        curr_square = -1000
        for j in range(i, len_str, WIDTH):
            if stringed_grid[j] == '#':
                curr_square = j
                highest_possible_idx = curr_square + WIDTH
            elif stringed_grid[j] == 'O':
                if j != highest_possible_idx:
                    curr_string = curr_string[:highest_possible_idx] + 'O' + \
                        curr_string[highest_possible_idx +
                                    1: j] + '.' + curr_string[j + 1:]
                highest_possible_idx += WIDTH

    # add the modified string to dict, reverse lookup gets added in the for loop

    return curr_string


def tilt_west(stringed_grid):
    # for tilting east west, since I don't need the entire
    # grid, can call tilt west on the substrings of size
    # WIDTH then recombine them after
    len_str = len(stringed_grid)
    shifted = []
    for i in range(0, len_str, WIDTH):
        # The i loop lets the j - loop create the vertical
        # lines
        mini_shifted = tilt_west_substring(stringed_grid[i: i + WIDTH])
        shifted.append(mini_shifted)

    curr_string = ''.join(shifted)
    return curr_string


def tilt_west_substring(substring):
    # called from tilt_west, given a string of size WIDTH
    # return a new string with the 'O' shifted west
    curr_square = -1
    highest_possible_idx = curr_square + 1
    curr_string = substring
    # assume this is being called properly
    for i in range(WIDTH):
        if substring[i] == '#':
            curr_square = i
            highest_possible_idx = curr_square + 1
        elif substring[i] == 'O':
            # rebuild the curr_string, shifting the current 'O' block
            if i != highest_possible_idx:
                curr_string = curr_string[:highest_possible_idx] + 'O' + \
                    curr_string[highest_possible_idx + 1: i] + \
                    '.' + curr_string[i + 1:]
            highest_possible_idx += 1

    return curr_string


def tilt_south(stringed_grid):
    len_str = len(stringed_grid)
    curr_string = stringed_grid
    for i in range(0, WIDTH, 1):
        # The i loop lets the j - loop create the vertical
        # lines
        curr_rock = -100
        insert_at = len_str - i - 1
        for j in range(len_str - i, 0, -WIDTH):
            idx = j - 1
            if stringed_grid[idx] == '#':
                # set the value of rock to j,
                # slideable slot to j + WIDTH
                curr_rock = idx
                insert_at = curr_rock - WIDTH
            elif stringed_grid[idx] == 'O':
                # rebuild curr_string since it's iterating
                # backwards the indexing is backwards
                if insert_at != idx:
                    curr_string = curr_string[:idx] + '.' + curr_string[idx +
                                                                        1: insert_at] + 'O' + curr_string[insert_at + 1:]
                insert_at -= WIDTH

    return curr_string


def tilt_east(stringed_grid):
    # for tilting east west, since I don't need the entire
    # grid, can call tilt west on the substrings of size
    # WIDTH then recombine them after
    len_str = len(stringed_grid)
    shifted = []
    for i in range(0, len_str, WIDTH):
        # The i loop lets the j - loop create the vertical
        # lines
        mini_shifted = tilt_east_substring(stringed_grid[i: i + WIDTH])
        shifted.append(mini_shifted)

    curr_string = ''.join(shifted)
    return curr_string


def tilt_east_substring(substring):
    # called from tilt_west, given a string of size WIDTH
    # return a new string with the 'O' shifted west
    curr_square = WIDTH
    insert_at = curr_square - 1
    curr_string = substring
    # assume this is being called properly
    for i in range(WIDTH, 0, -1):
        idx = i - 1
        if substring[idx] == '#':
            curr_square = idx
            insert_at = curr_square - 1
        elif substring[idx] == 'O':
            # rebuild the curr_string, shifting the current 'O' block
            if idx != insert_at:
                curr_string = curr_string[:idx] + '.' + curr_string[idx + 1:insert_at] + \
                    'O' + curr_string[insert_at + 1:]
            insert_at -= 1

    return curr_string


def print_grid(stringed):
    for i in range(HEIGHT):
        print(stringed[i * WIDTH: (i * WIDTH) + WIDTH])


# Have all of the functions defined, call spin_cycle(stringed_grid) to start
# go until the return value is in the dict already use modulo operator to find
# how deep to go into the cycle to get the last grid, then we'll do the
# math to get the northern load.

tilt_line_dict.clear()
curr_input = stringed_grid
count = 0
while curr_input not in tilt_line_dict and count < NUM_CYCLES:
    reverse_lookup[count] = curr_input
    new_input = spin_cycle(curr_input)
    tilt_line_dict[curr_input] = new_input
    print_grid(new_input)
    print('')
    curr_input = new_input
    count += 1

# found a loop or just went through the entire billion
# iterations and I lost my mind lol
# get the reverse lookup with the modulo thing
print(count)
input_to_find_load_idx = (count % NUM_CYCLES) - 1
print(input_to_find_load_idx)
input_find_load = reverse_lookup[input_to_find_load_idx]
print('')
print_grid(input_find_load)


# print_grid(tilt_east(stringed_grid))
# print(spin_cycle(stringed_grid))

def make_grid_from_string(stringed):
    grid = []
    for i in range(HEIGHT):
        grid.append(list(stringed[i * WIDTH: (i * WIDTH) + WIDTH]))

    return grid


def get_north_load(grid):
    count = 0
    for i in range(HEIGHT):
        count += (HEIGHT - i) * grid[i].count('O')

    return count


print(get_north_load(make_grid_from_string(input_find_load)))
