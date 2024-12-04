import sys

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 pt1.py puzzle_input.txt')
with open(sys.argv[1]) as open_file:
    lines = open_file.readlines()

LINES = lines

HEIGHT = len(lines)
WIDTH = len(lines[0])

WORD = 'XMAS'


def main():

    num_xmas = 0
    for y_idx, line in enumerate(LINES):
        for x_idx, char in enumerate(line):
            if char == 'X':
                num_xmas += find_all_from_x(x_idx, y_idx)

    print(num_xmas)
    return num_xmas


def find_all_from_x(x_index, y_index):
    running_total = 0
    # This is awful, surely there's a better way, was thinking defining to the
    # right and down, then flip the search space along both axes and rerun it?
    # might be better might be worse but this is disgusting
    if x_index < 3 and y_index < 3:
        # should only look to the right, down, and down-right
        running_total += find_to_right(x_index, y_index)
        running_total += find_to_bottom_right(x_index, y_index)
        running_total += find_to_below(x_index, y_index)
    elif x_index > WIDTH - 4 and y_index < 3:
        # should look to the left, down, and down-left
        running_total += find_to_left(x_index, y_index)
        running_total += find_to_bottom_left(x_index, y_index)
        running_total += find_to_below(x_index, y_index)
    elif x_index < 3 and y_index > HEIGHT - 4:
        # should look up, right, and up-right
        running_total += find_to_right(x_index, y_index)
        running_total += find_to_up_right(x_index, y_index)
        running_total += find_to_above(x_index, y_index)
    elif x_index > WIDTH - 4 and y_index > HEIGHT - 4:
        # should look up, left, and up-left
        running_total += find_to_left(x_index, y_index)
        running_total += find_to_up_left(x_index, y_index)
        running_total += find_to_above(x_index, y_index)
    elif x_index < 3:
        # can look down, above, right, up-right, down-right
        running_total += find_to_right(x_index, y_index)
        running_total += find_to_up_right(x_index, y_index)
        running_total += find_to_below(x_index, y_index)
        running_total += find_to_bottom_right(x_index, y_index)
        running_total += find_to_above(x_index, y_index)
    elif x_index > WIDTH - 4:
        # can look down, above, left, up-left, down-left
        running_total += find_to_left(x_index, y_index)
        running_total += find_to_up_left(x_index, y_index)
        running_total += find_to_above(x_index, y_index)
        running_total += find_to_bottom_left(x_index, y_index)
        running_total += find_to_below(x_index, y_index)
    elif y_index < 3:
        # can look left, right, down-left, down-right, down
        running_total += find_to_right(x_index, y_index)
        running_total += find_to_bottom_right(x_index, y_index)
        running_total += find_to_below(x_index, y_index)
        running_total += find_to_left(x_index, y_index)
        running_total += find_to_bottom_left(x_index, y_index)
    elif y_index > HEIGHT - 4:
        # can look left, right, up-left, up-right, up
        running_total += find_to_right(x_index, y_index)
        running_total += find_to_up_right(x_index, y_index)
        running_total += find_to_above(x_index, y_index)
        running_total += find_to_left(x_index, y_index)
        running_total += find_to_up_left(x_index, y_index)
    else:
        # should be able to get to every part of the search-space if it reaches
        # this point. I think. Should be 8 different directions possible
        running_total += find_to_right(x_index, y_index)
        running_total += find_to_up_right(x_index, y_index)
        running_total += find_to_above(x_index, y_index)
        running_total += find_to_left(x_index, y_index)
        running_total += find_to_up_left(x_index, y_index)
        running_total += find_to_bottom_left(x_index, y_index)
        running_total += find_to_below(x_index, y_index)
        running_total += find_to_bottom_right(x_index, y_index)

    return running_total


def find_to_above(x_idx, y_idx):
    # initial indices are the position of 'X' so skip it in the enumeration
    for i, char in enumerate(WORD):
        if i == 0:
            continue
        if not LINES[y_idx - i][x_idx] == WORD[i]:
            return 0
    print("called find_above")
    print("x_idx: ", x_idx, "y_idx: ", y_idx)
    return 1


def find_to_below(x_idx, y_idx):
    # initial indices are the position of 'X' so skip it in the enumeration
    for i, char in enumerate(WORD):
        if i == 0:
            continue
        if not LINES[y_idx + i][x_idx] == WORD[i]:
            return 0
    print("called find_to_below")
    print("x_idx: ", x_idx, "y_idx: ", y_idx)
    return 1


def find_to_right(x_idx, y_idx):
    # initial indices are the position of 'X' so skip it in the enumeration
    for i, char in enumerate(WORD):
        if i == 0:
            continue
        if not LINES[y_idx][x_idx + i] == WORD[i]:
            return 0
    print("called find_to_right")
    print("x_idx: ", x_idx, "y_idx: ", y_idx)
    return 1


def find_to_left(x_idx, y_idx):
    # initial indices are the position of 'X' so skip it in the enumeration
    for i, char in enumerate(WORD):
        if i == 0:
            continue
        if not LINES[y_idx][x_idx - i] == WORD[i]:
            return 0
    print("called find_to_left")
    print("x_idx: ", x_idx, "y_idx: ", y_idx)
    return 1


def find_to_up_right(x_idx, y_idx):
    # initial indices are the position of 'X' so skip it in the enumeration
    for i, char in enumerate(WORD):
        if i == 0:
            continue
        if not LINES[y_idx - i][x_idx + i] == WORD[i]:
            return 0
    print("called find_to_up_right")
    print("x_idx: ", x_idx, "y_idx: ", y_idx)
    return 1


def find_to_up_left(x_idx, y_idx):
    # initial indices are the position of 'X' so skip it in the enumeration
    for i, char in enumerate(WORD):
        if i == 0:
            continue
        if not LINES[y_idx - i][x_idx - i] == WORD[i]:
            return 0
    print("called find_to_up_left")
    print("x_idx: ", x_idx, "y_idx: ", y_idx)
    return 1


def find_to_bottom_right(x_idx, y_idx):
    # initial indices are the position of 'X' so skip it in the enumeration
    for i, char in enumerate(WORD):
        if i == 0:
            continue
        if not LINES[y_idx + i][x_idx + i] == WORD[i]:
            return 0
    print("called find_to_bottom_right")
    print("x_idx: ", x_idx, "y_idx: ", y_idx)
    return 1


def find_to_bottom_left(x_idx, y_idx):
    # initial indices are the position of 'X' so skip it in the enumeration
    for i, char in enumerate(WORD):
        if i == 0:
            continue
        if not LINES[y_idx + i][x_idx - i] == WORD[i]:
            return 0
    print("called find_to_bottom_left")
    print("x_idx: ", x_idx, "y_idx: ", y_idx)
    return 1


if __name__ == '__main__':
    main()
