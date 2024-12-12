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

starting_str = ""
curr_start_idx = 0
curr_data_id = 0
for i in range(line_len):
    if int(input_line[i]) == 0:
        continue
    if i % 2 == 0:
        # Even indices represent a data block
        id_data_blocks[curr_data_id] = [x for x in range(curr_start_idx,
                                        curr_start_idx + int(input_line[i]))]
        starting_str += str(curr_data_id) * int(input_line[i])
        curr_data_id += 1
    else:
        # data represents gap in between blocks
        empty_blocks.append([x for x in range(curr_start_idx,
                                              curr_start_idx +
                                              int(input_line[i]))])
        starting_str += "." * int(input_line[i])

    curr_start_idx += int(input_line[i])

# print(starting_str)
# Want to take right most value and place them into the left most empty block
# This fills in the empty blocks, now merge find the keys that are not in here
# to get the sum-product of the data id with the idx that it fills
curr_data_id -= 1
left_most_space = empty_blocks[0]
data = id_data_blocks[curr_data_id]

# print(empty_blocks)
for key in range(len(id_data_blocks.keys()) - 1, 0, -1):
    # len of the file chunk intended to be moved:
    file_len = len(id_data_blocks[key])
    empty_block_idx = 0
    inserted = False
    while empty_block_idx < len(empty_blocks) - 1 and not inserted:
        cur_empty_block_len = len(empty_blocks[empty_block_idx])
        # print("Empty len: ", cur_empty_block_len, " empty idx: ",
        #       empty_block_idx, " file len: ", file_len)
        if (cur_empty_block_len >= file_len and
                not empty_blocks[empty_block_idx][0] > id_data_blocks[key][0]):
            # insert file into the block
            # print("Should be inserting hello!")
            # print(" BEGIN INSERT ------------------")
            compressed_locations[key] = (
                empty_blocks[empty_block_idx][:file_len]
            )
            # print(compressed_locations)
            empty_blocks[empty_block_idx] = (
                empty_blocks[empty_block_idx][file_len:]
            )
            # print(empty_blocks)
            inserted = True
            # print(" END INSERT ------------------")
        else:
            empty_block_idx += 1


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

print(to_modify)
print(checksum_value)
