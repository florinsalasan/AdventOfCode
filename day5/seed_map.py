import sys


def main():
    # similar idea as part one, need to maintain the max values
    # for each line now
    if (len(sys.argv) != 2):
        sys.exit('Usage: python3 seed_map.py puzzle_input')
    # list out the entirety of the file line by line
    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    lists_to_map = []
    for line in lines:
        if line == lines[0]:
            seeds = line
        if line == '\n':
            continue
        print(list(line)[0])
        if not list(line)[0].isdigit():
            lists_to_map.append([])
        lists_to_map[len(lists_to_map) - 1].append(line)

    print(lists_to_map)


if __name__ == "__main__":
    main()
