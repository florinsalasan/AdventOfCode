import sys

# same technique as part 1, just need to change the input slightly
# never mind, this would take for ever if it was just raw input
# generating the seeds takes forever too, new plan, create something
# to reach the location, then find a way to get the break points
# where each range of seeds gets a different path to location delta
# find the smallest location for the break points because I just
# noticed how ridiculously large the num of seeds will be, just
# checked, would be ~1.7 billion, so iterating through them all
# is just not feasible so break down the problem, say we have
# seed entry of 5 10, then 5 - 14 need to be ran through the mapping
# if 5 - 10 fits one mapping while 11-14 fits another just pass that
# into the next map.


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
    seed_list = lists_to_map[0]
    seed_list = seed_list[0].split()
    seed_list = seed_list[1:]

    seed_pairs = []
    for i, seed_pair in enumerate(seed_list):
        if i % 2 == 0:
            seed_pairs.append([int(seed_pair), int(
                seed_pair) + int(seed_list[i + 1]) - 1])

    mapped_lists = {}

    lists_to_map = lists_to_map[1:]
    sorted_inner = []
    for map in lists_to_map:
        list_of_splits = []
        for mapping in map:
            split_mapping = mapping.split()
            list_of_splits.append(split_mapping)
        for i in range(len(list_of_splits)):
            for j in range(len(list_of_splits) - 1 - i):
                if (list_of_splits[j][1] > list_of_splits[j + 1][1]):
                    temp = list_of_splits[j]
                    list_of_splits[j] = list_of_splits[j + 1]
                    list_of_splits[j + 1] = temp

        # list_of_splits[-1] is the title of the map ie soil-to-temp
        sorted_inner.append(list_of_splits)
    # want to sort the mappings themselves within the bigger list
    # by source

    for i, list_to_map in enumerate(sorted_inner):
        mapped_lists[i] = []
        for map in list_to_map:
            if not map[0].isdigit():
                continue
            mapped_lists[i].append({
                'destination': int(map[0]),
                'source': int(map[1]),
                'range_len': int(map[2]),
            })

    # mapped_lists now is a dict where the keys are ints equal to the number of
    # maps passed into the input, assumes the maps are ordered in the input,
    # though to expand would be a better idea to have them properly ordered
    # programatically with the type-to-type header each map has for safety.
    # But since I'm already behind, will just sanitize any input before hand
    # if testing other configs. each value for a given key is a list of dicts
    # that has the destination, source, and range_len as keys to then split
    # the incoming seed_pairs

    # overall plan, for each map, want to go through the seed buckets and update
    # the list of them to the new values based on destination and create any
    # new buckets that might be needed for the next map.

    for i in range(len(mapped_lists.keys())):
        for seed_bucket in seed_pairs:
            delta = 0
            modified = False
            for mapping in mapped_lists[i]:
                if seed_bucket[0] >= mapping['source'] and seed_bucket[0] < mapping['source'] + mapping['range_len'] and not modified:
                    # this is the case where the bucket at least partially fits in the mapping bucket
                    delta = mapping['destination'] - mapping['source']
                    if (seed_bucket[1] <
                            mapping['source'] + mapping['range_len']):
                        # entire bucket fits in this mapping, just apply
                        # the delta to both values in seed_bucket
                        seed_bucket[0] += delta
                        seed_bucket[1] += delta
                    else:
                        # need to split the bucket into two buckets,
                        # current bucket gets it's high end updated to
                        # mapping source + rangelen - 1, new bucket is
                        # mapping source + rangelen, seed_bucket[1] and is
                        # appended to the seed_pairs, should continue splitting
                        # buckets until it is no longer needed and can move onto
                        # the next map
                        # I'm dumb, need the scenario where there is no map the bucket falls into
                        new_bucket = [
                            mapping['source'] + mapping['range_len'],
                            seed_bucket[1]
                        ]
                        seed_pairs.append(new_bucket)
                        seed_bucket[1] = mapping['source'] + \
                            mapping['range_len'] - 1
                        seed_bucket[0] += delta
                        seed_bucket[1] += delta
                    modified = True

    sorted_pairs = []
    for pair in seed_pairs:
        sorted_pairs.append(pair[0])
    print(min(sorted_pairs))
    return sorted_pairs


if __name__ == "__main__":
    main()
