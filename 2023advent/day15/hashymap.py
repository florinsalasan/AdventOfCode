import sys
import csv


if (len(sys.argv) != 2):
    sys.exit('Usage: python hash.py input.csv')


# Read it in with csv dict reader or something, basically check documentation
values = []
with open(sys.argv[1]) as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        for item in row:
            values.append(item)

# now need to get the label from each value in values
# Running hash from part1 gives a number between 0-255
# to place the lens into or remove from box. Don't feel
# like including a key check for each box number so
# I generated all 256 boxes.

hashymap = {}

for i in range(256):
    hashymap[i] = [{}, []]


def breakdown_value(value):
    if '-' in value:
        items = value.split('-')
        box_num = hash(items[0])
        to_remove = items[0]
        remove(box_num, to_remove)
    else:
        items = value.split('=')
        box_num = hash(items[0])
        to_insert = (items[0], int(items[1]))
        insert(box_num, to_insert)


def insert(box_num, lens):
    # given the box_num and the lens insert into the hashymap
    # can only have one lens of the same label in a box so
    # first step is seeing if a lens needs to be replaced or
    # simply inserted into the hashymap
    box_of_lenses = hashymap[box_num]

    # each box will have a list of len 2, first item is a
    # dict containing information of the labels in the list
    # the list contains all of the lenses
    if lens[0] in box_of_lenses[0]:
        # replace the lens in the list at box_of_lenses[1]
        # get idx of the label in the list
        idx_to_swap = box_of_lenses[0][lens[0]]
        modify_this = box_of_lenses[1]
        modify_this = modify_this[:idx_to_swap] + \
            [[lens[0], lens[1]]] + modify_this[idx_to_swap + 1:]

        hashymap[box_num] = [box_of_lenses[0], modify_this]

    else:
        # append to the list of the lenses, add the label and idx to the dict
        # that lets us check if the label already is in use.
        idx_inserted_at = len(box_of_lenses[1])
        hashymap[box_num][1].append([lens[0], lens[1]])
        hashymap[box_num][0][lens[0]] = idx_inserted_at


def remove(box_num, lens):
    # given the box_num and the lens remove from the hashymap
    # then update the index of the remaining lenses in the dict
    if lens not in hashymap[box_num][0]:
        return
    # first get index of where the lens is
    idx = hashymap[box_num][0][lens]

    # modify the list with slicing
    modify_this = hashymap[box_num][1]
    modify_this = modify_this[:idx] + modify_this[idx + 1:]
    hashymap[box_num][1] = modify_this

    # remove the label from the dict
    del hashymap[box_num][0][lens]

    # change the idxs stored in the dict
    for key in hashymap[box_num][0].keys():
        curr_idx = hashymap[box_num][0][key]
        if curr_idx > idx:
            hashymap[box_num][0][key] -= 1


def hash(str_input):
    # returns a value based on the HASH algorithm described in the
    # specs, add the ASCII value of the char to the starting value,
    # multiply it by 17, take that product and mod by 256 to get the
    # next characters starting value

    starting_value = 0

    for code in str_input.encode('ascii'):
        curr_value = starting_value + code
        curr_value *= 17
        curr_value = curr_value % 256
        starting_value = curr_value

    return starting_value


for value in values:
    breakdown_value(value)


# the hashymap will have been fully modified and gone through the entire file
# by reaching this point

focusing_power = 0

for key in hashymap.keys():
    for lens_idx, lens in enumerate(hashymap[key][1]):
        # don't need to check the idx from the dict
        # since we'll just be going in order anyways
        focusing_power += (key + 1) * (lens_idx + 1) * lens[1]

print(focusing_power)
