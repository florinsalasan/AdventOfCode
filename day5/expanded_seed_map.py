import sys

# same technique as part 1, just need to change the input slightly
# never mind, this would take for ever if it was just raw input


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python3 seed_map.py puzzle_input')
    # list out the entirety of the file line by line
    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    lists_to_map = []
    for line in lines:
        if line == '\n':
            continue
        if not list(line)[0].isdigit():
            lists_to_map.append([])
        lists_to_map[len(lists_to_map) - 1].append(line)

    # for each line now
    seed_pairs = lists_to_map[0]
    seed_pairs = seed_pairs[0].split()
    seed_pairs = seed_pairs[1:]

    seeds = []
    for i, seed_pair in enumerate(seed_pairs):
        if i % 2 == 0:
            for j in range(int(seed_pairs[i + 1])):
                seeds.append(int(seed_pair) + j)

    print(seed_pairs)
    print(seeds)
    seed_to_location = {}

    for seed in seeds:
        curr_seed = int(seed)
        # walk the seed through the lists_to_map to get the input
        # for the next map
        ith_map = 1
        curr_input = curr_seed
        while ith_map < len(lists_to_map):
            delta = 0
            for maps in lists_to_map[ith_map]:
                maps = maps.split()
                if not maps[0].isdigit():
                    continue
                destination = int(maps[0])
                source = int(maps[1])
                range_len = int(maps[2])
                if (curr_input >= source and
                        curr_input < source + range_len):
                    delta = destination - source
                else:
                    continue
                # changes curr_input if mapped, otherwise
                # leave as is to use in next map
            curr_input += delta

            ith_map += 1
        # Once it goes through all of the mappings,
        # create the seed to location entry
        seed_to_location[curr_seed] = curr_input

    # have the seed to location dictionary, get the smallest location
    # value from the dictionary values

    print(seed_to_location)
    print(min(seed_to_location.values()))


if __name__ == "__main__":
    main()
