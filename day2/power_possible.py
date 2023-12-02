import sys


def main():
    # similar idea as part one, need to maintain the max values
    # for each line now
    if (len(sys.argv) != 2):
        sys.exit('Usage: python3 possible.py puzzle_input')
    # list out the entirety of the file line by line
    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    power_possible_sum = 0
    # instead of having a dictionary with the known amount of cubes
    # have a separate dictionary for each line containing the max
    # number we found for each colour, then multiply them together
    # before adding them to the running sum

    for line in lines:
        # if line == lines[-1]:
        #    break
        words = line.split()
        # for this words 0, 1 are useless, and then we do a similar loop
        # where we start at index 2, up to len(words) - 2, by 2
        # no example was given if a certain colour isn't drawn but by the
        # given ruleset the power for that game would be 0
        min_needed = {
            'red': 0,
            'green': 0,
            'blue': 0,
        }

        for i in range(2, len(words) - 1, 2):
            # changed range to len(words) - 1 since it was not
            # reading the final number of coloured cubes that was pulled
            # in each game, making me think I just got lucky in pt 1
            # rather than getting the right answer on purpose.
            # tried to change it in pt 1 and got a key error so I
            # must have done something right
            if (words[i + 1][-1] == ';' or words[i + 1][-1] == ','):
                if int(words[i]) > min_needed[words[i + 1][: -1]]:
                    min_needed[words[i + 1][: -1]] = int(words[i])
            else:
                if int(words[i]) > min_needed[words[i + 1]]:
                    min_needed[words[i + 1]] = int(words[i])

        power = 1
        for value in min_needed.values():
            power *= value

        power_possible_sum += power

    print(power_possible_sum)
    return power_possible_sum


if __name__ == "__main__":
    main()
