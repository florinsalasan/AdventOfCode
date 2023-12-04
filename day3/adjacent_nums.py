import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python adjacent_nums.py input_file')

    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    # have the list of lines, need to create the conditionals where
    # a number is adjacent to a symbol that is not '.', diagonal
    # connections count as well.
    sum = 0

    for line_idx, line in enumerate(lines):
        if line == lines[-1]:
            break
        # loop over string to find numbers
        list_line = list(line)
        list_line = list_line[:-1]
        for item_idx, item in enumerate(list_line):
            if item.isdigit():
                # get indices of the number
                indices = get_num(list_line, item_idx)
                to_check = [max(indices[0] - 1, 0),
                            min(indices[1] + 1, len(list_line) - 1)]
                touching_symbol = False
                if indices[0] - 1 >= 0 and list_line[indices[0] - 1] != '.':
                    touching_symbol = True
                if (indices[1] + 1 < len(list_line) and
                        list_line[indices[1] + 1] != '.'):
                    touching_symbol = True
                if (line_idx - 1 >= 0 and
                        touching(lines[line_idx - 1], to_check)):
                    touching_symbol = True
                # when checking for last line remember that the last line is
                # blank so len(lines) - 1 for the last line with data
                if (line_idx + 1 < len(lines) - 1 and
                        touching(lines[line_idx + 1], to_check)):
                    touching_symbol = True
                if touching_symbol:
                    sum += int(''.join(list_line[indices[0]:indices[1] + 1]))
                # remove the number from the list to not look for symbols
                # around it multiple times
                curr_idx = indices[0]
                while curr_idx <= indices[1]:
                    list_line[curr_idx] = '.'
                    curr_idx += 1
    print(sum)
    return sum


def get_num(line, start_idx):
    curr_idx = start_idx
    while curr_idx < len(line) and line[curr_idx].isdigit():
        curr_idx += 1
    return [start_idx, curr_idx - 1]


def touching(line, search_indices):
    curr_idx = search_indices[0]
    touched = False
    while curr_idx <= search_indices[1] and not touched:
        if line[curr_idx] != '.' and not line[curr_idx].isdigit():
            touched = True
        curr_idx += 1
    return touched


if __name__ == "__main__":
    main()
