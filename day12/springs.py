import sys


def main():

    if (len(sys.argv) != 2):
        sys.exit('Usage: python springs.py input.txt')

    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    if lines[-1] == '\n':
        lines = lines[:-1]

    tupled_lines = []
    for line in lines:
        line_listed = list(line.split()[0])
        str_list_of_broken_lens = list(line.split()[1])
        list_of_broken_lens = []
        for item in str_list_of_broken_lens:
            if item.isdigit():
                list_of_broken_lens.append(int(item))
        tupled_lines.append((line_listed, list_of_broken_lens))

    permutations = {}

    # Genuinely unsure of how to set up the permutation calculations,
    # figure I need to do some recursion and maybe memoization if the
    # input ends up being too crazy, but I can't think of the base cases,
    # or how to properly recurse for the remaining cases.

    # So the breakdown into smaller pieces would be shortening the input line
    # if the first char is '.' since it is irrelevant. Then if it is a '?' check
    # what happens if turning it into '#'. Need to do a check now if it's possible
    # to fit the first broken length in the newly created series of '#'s if not,
    # then it should return 0 + count_permutations(str[1:], lens) if it can be fit
    # in, then 1 + count_permutations(str[lens[0]:], lens[1:])


if __name__ == "__main__":
    main()
