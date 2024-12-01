import sys

# identical problem as part1, just need to modify the input slightly

if (len(sys.argv) != 2):
    sys.exit('Usage: python unfolded.py input.txt')

with open(sys.argv[1]) as open_file:
    lines = open_file.readlines()

if lines[-1] == '\n':
    lines = lines[:-1]

# create the input by 5x both pieces
tupled_lines = []
for line in lines:
    spring_row, broken_lens = line.split()
    # have the two strings, now multiply them by 5 essentially
    # first attach the char that separates the multiple string
    # counts.
    spring_row += '?'
    broken_lens += ','
    # multiply the strings by 5
    spring_row *= 5
    broken_lens *= 5
    # remove the last char since it is a seperator char that
    # is unnecessary
    spring_row = spring_row[:-1]
    broken_lens = broken_lens[:-1]

    int_broken_lens = []
    for length in broken_lens.split(','):
        int_broken_lens.append(int(length))

    tupled_lines.append((list(spring_row), int_broken_lens))

# have a list of tuples containing the spring and the
# lengths of the broken sections
# now just recreate the dynamic programming solution from pt1
# and rerun it for the expanded spring_input

cache = {}


def find_counts(spring_input, damaged_lens, spring_idx, damaged_idx, curr_damaged_len):
    curr_key = (spring_idx, damaged_idx, curr_damaged_len)
    # check if the current value has already been calculated and return it if it has
    if curr_key in cache:
        return cache[curr_key]
    # if not in cache, create the base cases
    if spring_idx == len(spring_input):
        # cleared all of the damaged lengths described so return 1
        if damaged_idx == len(damaged_lens) and curr_damaged_len == 0:
            return 1
        # on the last damaged block, check if we reached the same length as was listed
        # if so there's only one possible permutation so return 1
        elif damaged_idx == len(damaged_lens) - 1 and damaged_lens[damaged_idx] == curr_damaged_len:
            return 1
        # no other way to get a valid entry if reaching here so return 0
        else:
            return 0
    # if we haven't gone through the entire row of spring_input, do the recursive calls
    count = 0
    for possible_char in ['.', '#']:
        # This treats both the current character and '?' as the same value for this instance
        # of a recursive call
        if spring_input[spring_idx] == possible_char or spring_input[spring_idx] == '?':
            # continue looking for the next block of damaged spring_input
            if possible_char == '.' and curr_damaged_len == 0:
                count += find_counts(spring_input, damaged_lens,
                                     spring_idx + 1, damaged_idx, 0)
            # found the end of the damaged block of spring_input
            elif (curr_damaged_len > 0
                    and possible_char == '.'
                    and damaged_idx < len(damaged_lens)
                    and damaged_lens[damaged_idx] == curr_damaged_len):
                count += find_counts(spring_input, damaged_lens,
                                     spring_idx + 1, damaged_idx + 1, 0)
            # continue until the end of the damaged block
            elif possible_char == '#':
                count += find_counts(spring_input, damaged_lens,
                                     spring_idx + 1, damaged_idx, curr_damaged_len + 1)

    cache[curr_key] = count
    return count


num_permutations = 0
for pair in tupled_lines:
    cache.clear()
    score = find_counts(pair[0], pair[1], 0, 0, 0)
    num_permutations += score

print(num_permutations)
