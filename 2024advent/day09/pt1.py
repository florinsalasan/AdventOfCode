import sys

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 pt1.py puzzle_input.txt')
with open(sys.argv[1]) as open_file:
    lines = open_file.readlines()

input_line = lines[0]

# remove the newline character
line_len = len(input_line[:-1])
list_line = list(input_line)
list_line_total_len = 0
for str_value in list_line[:-1]:
    list_line_total_len += int(str_value)

id_data_blocks = {}
empty_blocks = []
compressed_locations = {}

curr_start_idx = 0
curr_data_id = 0
for i in range(line_len):
    if int(input_line[i]) == 0:
        continue
    if i % 2 == 0:
        # Even indices represent a data block
        id_data_blocks[curr_data_id] = [x for x in range(curr_start_idx,
                                        curr_start_idx + int(input_line[i]))]
        curr_data_id += 1
    else:
        # data represents gap in between blocks
        empty_blocks += [x for x in range(curr_start_idx,
                                          curr_start_idx + int(input_line[i]))]

    curr_start_idx += int(input_line[i])

last_filled_idx = 0

# Want to take right most value and place them into the left most empty block
# This fills in the empty blocks, now merge find the keys that are not in here
# to get the sum-product of the data id with the idx that it fills
curr_data_id -= 1
left_most_space = empty_blocks[0]
data = id_data_blocks[curr_data_id]
lower, right_most_data = data[0], data[-1]

while right_most_data > left_most_space:
    left_most_space = empty_blocks[0]
    if curr_data_id not in compressed_locations.keys():
        compressed_locations[curr_data_id] = [left_most_space]
    else:
        compressed_locations[curr_data_id].append(left_most_space)
    empty_blocks = empty_blocks[1:]
    left_most_space = empty_blocks[0]
    right_most_data -= 1
    if right_most_data < lower:
        curr_data_id -= 1
        data = id_data_blocks[curr_data_id]
        lower, right_most_data = data[0], data[-1]

for key in compressed_locations.keys():
    if len(compressed_locations[key]) != len(id_data_blocks[key]):
        to_append = id_data_blocks[key][:-len(compressed_locations[key])]
        compressed_locations[key] += to_append

to_modify = "." * list_line_total_len
checksum_value = 0
for key in compressed_locations.keys():
    for value in compressed_locations[key]:
        to_modify = to_modify[:value] + str(key) + to_modify[value + 1:]
        checksum_value += value * key

for other_key in id_data_blocks.keys():
    if other_key not in compressed_locations.keys():
        for value in id_data_blocks[other_key]:
            to_modify = (to_modify[:value] + str(other_key) +
                         to_modify[value + 1:])
            checksum_value += value * other_key

print(checksum_value)
