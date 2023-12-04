import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python adjacent_nums.py input_file')

    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    sum = 0
    for line in lines:
        values = line.split(' ')
        # remove newline character at the end of the last number in the list
        values[-1] = values[-1][:-1]
        # remove the first two values of the list since they are just the card#
        values = values[2:]
        # want to remove any '' blanks from a number that was less than 10
        while '' in values:
            values.remove('')
        # now find the index of '|' and separate the lists into two parts
        # the items that are before the '|' are the scratch card, then ones
        # after are the winning numbers to check against
        split_idx = values.index('|')
        scratch_card = values[: split_idx]
        winning_numbers = values[split_idx + 1:]
        num_winning = 0

        for num in scratch_card:
            if num in winning_numbers:
                num_winning += 1

        if num_winning == 1:
            sum += 1
        if num_winning > 1:
            sum += 2 ** (num_winning - 1)

    print(sum)
    return sum


if __name__ == "__main__":
    main()
