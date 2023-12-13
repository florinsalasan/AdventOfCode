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


if __name__ == "__main__":
    main()
