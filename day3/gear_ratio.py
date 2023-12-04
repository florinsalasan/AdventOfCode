import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python adjacent_nums.py input_file')

    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    sum = 0
    # to find gear ratios need to look for two numbers
    # that are adjacent to '*' so look for '*' first
    # then check if it has exactly two numbers adjacent

    for line_idx, line in enumerate(lines):
        line_list = list(line)
        line_list = line_list[:-1]
        for char_idx, char in enumerate(line_list):
            if char == '*':
                adj_nums = adjacent_nums(line_list, line_idx, char_idx, lines)
                if len(adj_nums) == 2:
                    sum += int(adj_nums[0]) * int(adj_nums[1])

    print(sum)
    return sum


def adjacent_nums(line_list, line_idx, char_idx, lines):
    adj_nums = []
    # check to the left and to the right of char_idx in the line
    curr_idx = char_idx - 1
    num_builder = []
    # searching to the left
    while curr_idx >= 0 and line_list[curr_idx].isdigit():
        num_builder = [line_list[curr_idx]] + num_builder
        curr_idx -= 1
    if len(num_builder) > 0:
        temp = [int(''.join(num_builder))]
        num_builder = []
        adj_nums.append(temp)
    # searching to the right
    curr_idx = char_idx + 1
    while curr_idx < len(line_list) and line_list[curr_idx].isdigit():
        num_builder.append(line_list[curr_idx])
        curr_idx += 1
    if len(num_builder) > 0:
        temp = [int(''.join(num_builder))]
        num_builder = []
        adj_nums.append(temp)
    curr_idx = char_idx
    # check above for numbers:
    if line_idx != 0:
        above_list = list(lines[line_idx - 1])
        adj_nums.append(get_nums_in_row(above_list, char_idx))
    if line_idx != len(lines) - 2:
        below_list = list(lines[line_idx + 1])
        adj_nums.append(get_nums_in_row(below_list, char_idx))
    flat_list = [item for sublist in adj_nums for item in sublist]
    return (flat_list)


def get_nums_in_row(given_list, char_idx):
    adj_nums = []
    if char_idx - 1 >= 0 and given_list[char_idx - 1].isdigit():
        # check if theres a digit at char_idx and at char_idx + 1
        if given_list[char_idx].isdigit():
            if (char_idx + 1 < len(given_list) and
                    given_list[char_idx + 1].isdigit()):
                # at most one number above the gear, find the edges
                curr_idx = char_idx + 1
                right_side = [given_list[char_idx]]
                while curr_idx < len(given_list) and given_list[curr_idx].isdigit():
                    right_side.append(given_list[curr_idx])
                    curr_idx += 1
                left_side = []
                curr_idx = char_idx - 1
                while curr_idx >= 0 and given_list[curr_idx].isdigit():
                    left_side = [given_list[curr_idx]] + left_side
                    curr_idx -= 1
                num_list = left_side + right_side
                if len(num_list) > 0:
                    num = int(''.join(num_list))
                    adj_nums.append(num)
            else:
                # number ends at char_idx, find the left edge
                left_side = [given_list[char_idx]]
                curr_idx = char_idx - 1
                while curr_idx >= 0 and given_list[curr_idx].isdigit():
                    left_side = [given_list[curr_idx]] + left_side
                    curr_idx -= 1
                num = int(''.join(left_side))
                adj_nums.append(num)
        else:
            # number ends at char_idx - 1, find left edge
            left_side = []
            curr_idx = char_idx - 1
            while curr_idx >= 0 and given_list[curr_idx].isdigit():
                left_side = [given_list[curr_idx]] + left_side
                curr_idx -= 1
                # know char_idx - 1 is a digit so num has to not be empty
            num = int(''.join(left_side))
            adj_nums.append(num)
            # need to check if a different number exists starting at char_idx + 1, know
            # there is no digit at char_idx so just check for separation
            if char_idx + 1 < len(given_list) and given_list[char_idx + 1].isdigit():
                curr_idx = char_idx + 1
                num_builder = []
                while curr_idx < len(given_list) and given_list[curr_idx].isdigit():
                    num_builder.append(given_list[curr_idx])
                    curr_idx += 1
                num = int(''.join(num_builder))
                adj_nums.append(num)

    elif given_list[char_idx].isdigit():
        # num starts at char idx, only need to find where the num ends
        curr_idx = char_idx
        num_builder = []
        while curr_idx < len(given_list) and given_list[curr_idx].isdigit():
            num_builder.append(given_list[curr_idx])
            curr_idx += 1
        num = int(''.join(num_builder))
        adj_nums.append(num)
    elif char_idx + 1 < len(given_list) and given_list[char_idx + 1].isdigit():
        # num starts at char_idx + 1, know the other 2 possible indexes do not have
        # digits so only need to find what number this is
        curr_idx = char_idx + 1
        num_builder = []
        while curr_idx < len(given_list) and given_list[curr_idx].isdigit():
            num_builder.append(given_list[curr_idx])
            curr_idx += 1
        num = int(''.join(num_builder))
        adj_nums.append(num)

    return adj_nums


if __name__ == "__main__":
    main()
