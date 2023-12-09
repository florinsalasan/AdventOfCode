import sys


def main():

    if (len(sys.argv) != 2):
        sys.exit("Usage: python find_patterns.py input.txt")

    with open(sys.argv[1]) as input_file:
        lines = input_file.readlines()

    if lines[-1] == '\n':
        lines = lines[:-1]

    sum = 0
    for line in lines:
        diff_lists = []
        curr_line = line.split()
        solved = False
        while not solved:
            curr_diffs = []
            for i in range(len(curr_line) - 1):
                curr_diffs.append(
                    (-(int(curr_line[i]) - int(curr_line[i + 1]))))
            if curr_diffs.count(0) == len(curr_line) - 1:
                solved = True
                diff_lists.append(curr_diffs)
            else:
                curr_line = curr_diffs
                diff_lists.append(curr_diffs)
        # By this point should have a list of diff_lists, with the last one being all the same
        # number, since we only append if the list is not all 0s, so then need to append to
        # diff lists the last item in the list plus the last item in the previous list
        idx = len(diff_lists) - 1
        print(diff_lists)
        while idx != 0:
            diff_to_minus = diff_lists[idx][0]
            diff_lists[idx - 1] = [diff_lists[idx - 1]
                                   [0] - diff_to_minus] + diff_lists[idx - 1]
            idx -= 1
        # All of the diff_lists have had the next difference appended, just need to make the
        # prediction on the current line and then add it to the sum
        print(diff_lists)
        split_line = line.split()
        sum += int(split_line[0]) - diff_lists[0][0]

    print(sum)
    return sum


if __name__ == "__main__":
    main()
