import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python3 possible.py puzzle_input')
    # list out the entirety of the file line by line
    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    possible_sum = 0

    cube_nums = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    for line in lines:
        if line == lines[-1]:
            # last line is a blank line, easiest way I found of dealing with it
            break
        # want to split each line into an array of strings
        # so use .split method
        words = line.split()
        # the words still have the punctuation attached which
        # we use to grab the current game num,
        # don't need to worry about different pulls, just ensure
        # that max number of marbles for each colour does not
        # exceed the ones defined in cube_nums
        # words[1] will be the game number with ':' attached slice
        # it so that it takes everything upto but not including the :

        curr_num = int(words[1][:-1])
        possible = True

        for i in range(2, len(words) - 2, 2):
            # len(words) - 2 because we only want to go to 2nd last
            # since we always look for i + 1 to give the colour
            # even num i will be an index that gives a value, i + 1
            # will give the related colour
            curr_value = int(words[i])
            if curr_value > cube_nums[words[i + 1][:-1]]:
                possible = False

        if possible is True:
            possible_sum += curr_num

    print(possible_sum)
    return possible_sum


if __name__ == "__main__":
    main()
