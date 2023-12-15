# Thanks to u/jonathan_paulson for the video describing your solution, it really helped me
# understand how to break the problem down into smaller pieces to allow for the
# memoization of the sub problems.

import sys
import math

if (len(sys.argv) != 2):
    sys.exit('Usage: python springs.py input.txt')

with open(sys.argv[1]) as open_file:
    lines = open_file.readlines()

if lines[-1] == '\n':
    lines = lines[:-1]

tupled_springs = []

for line in lines:
    new_line = line.split()
    spring_row = list(new_line[0])
    broken_lens = new_line[1].split(',')
    spring_lens = []
    for item_idx, item in enumerate(broken_lens):
        spring_lens.append(int(item))
    new_spring = (tuple(spring_row), tuple(spring_lens))

    tupled_springs.append(new_spring)

# now have a list of tuples that contain the input row of springs, and the
# tuple of lens of contiguous broken springs.
cache = {}


def find_count(spring_row, broken_blocks, spring_idx, block_idx, current_block_length):
    # spring_row is the list of symbols indicating the spring condition,
    # broken_blocks, is the list of contiguous broken springs that comes after the springs
    # spring idx, index of where we are in the input,
    # block_idx, which block we are on in broken_blocks,
    # current_block_length, the value of broken_blocks[block_idx]

    curr_key = (spring_idx, block_idx, current_block_length)
    # check if we already know and stored the value, if so return it
    if curr_key in cache:
        return cache[curr_key]
    # create the base cases, or the smallest problems to build other
    # answers off of
    # check if we reached the end of the input
    if spring_idx == len(spring_row):
        # check if we also checked all of the blocks
        if block_idx == len(broken_blocks) and current_block_length == 0:
            # validated the whole input, nothing left to do but return 1
            return 1
        elif block_idx == len(broken_blocks) - 1 and broken_blocks[block_idx] == current_block_length:
            # on the last block, if the block length is as long as expected only
            # one possible permutation so return 1
            return 1
        else:
            # any other block_idx or broken_blocks value would not be a valid
            # entry so return 0 in this case.
            return 0
    count = 0
    for possible_char in ['.', '#']:
        # check below essentially sets ? to whichever of the possible_chars we're
        # currently on
        if spring_row[spring_idx] == possible_char or spring_row[spring_idx] == '?':
            if possible_char == '.' and current_block_length == 0:
                # currently not on a broken block so increment the character we're checking
                # and run the function again.
                count += find_count(spring_row, broken_blocks,
                                    spring_idx + 1, block_idx, 0)
            elif (possible_char == '.'
                    and current_block_length > 0
                    and block_idx < len(broken_blocks)
                    and broken_blocks[block_idx] == current_block_length):
                # found the end of a contiguous broken block of springs, so increment the
                # character idx in spring_row and which block we're checking next.
                count += find_count(spring_row, broken_blocks,
                                    spring_idx + 1, block_idx + 1, 0)
            elif possible_char == '#':
                # continue counting how long the block of broken springs is.
                count += find_count(spring_row, broken_blocks,
                                    spring_idx + 1, block_idx, current_block_length + 1)
    cache[curr_key] = count
    return count


num_permutations = 0
for pair in tupled_springs:
    cache.clear()
    score = find_count(pair[0], pair[1], 0, 0, 0)
    num_permutations += score


print(num_permutations)
