import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python imaging_multithreading.py puzzle_input.txt')

    with open(sys.argv[1]) as input_file:
        lines = input_file.readlines()

    path = lines[0]
    path = path[:-1]

    node_to_nodes = {}
    rl_to_idx = {
        'L': 0,
        'R': 1,
    }

    starting_nodes = []
    # who knows how many times we'll have to access the nodes,
    # so create a dict early once by looping over the lines once
    for line_idx, line in enumerate(lines):
        if line_idx == 0:
            continue
        if line == '\n':
            continue
        else:
            new_line = line.split('=')
            stripped_items = []
            for item in new_line:
                stripped_items.append(item.strip())
            # stripped_items[0] is the key to use for the tuples
            # that will be made next
            # subitems slicing will always be the same since it
            # is always a len of 3 for the nodes, this just strips
            # the nodes of '(', ')' and ,','
            new_subitems = [
                stripped_items[1][1:4],
                stripped_items[1][6:-1],
            ]

            node_to_nodes[stripped_items[0]] = new_subitems
            if stripped_items[0][2] == 'A':
                starting_nodes.append(stripped_items[0])

    # now that there are multiple nodes to traverse at once need to slightly
    # modify the traversal and end check uhm so need to revisit the logic here
    # Seemingly trying to do all of the paths at once until it reaches the end
    # is not the play here. Instead how about we run the part 1 algo for
    # each starting_node and go from there.
    counts = []
    for node in starting_nodes:
        found = False
        i = 0
        count = 0
        curr_node = node
        while not found:
            # for i in range(3):
            curr_node = node_to_nodes[curr_node][rl_to_idx[path[i]]]
            count += 1
            if curr_node[2] == 'Z':
                found = True
            else:
                i = (i + 1) % (len(path))
        counts.append(count)

    # have the count needed for each possible starting node to reach the end. so given that
    # these repeat until they are all on a node that ends in a 'Z', need to find the number
    # where it is divisible by all of the counts, know for sure that it is less than or equal
    # to all of the counts multiplied together.
    lowest_possible_count = get_lowest_common_multiple(counts)
    print(lowest_possible_count)
    # the answer is ridculous, final count is > 10000000000000, would have been
    # impossible to brute force it lol
    return lowest_possible_count


def get_lowest_common_multiple(counts):
    # this is the base case, do prime factorization for the two nums,
    # doing this recursively is dumb now that i think about it, would
    # be heavy compute to get prime factors every time.
    prime_factors = []
    for item in counts:
        prime_factors.append(prime_factorize(item))
    biggest_powers = {}
    for prime_dict in prime_factors:
        for prime in prime_dict.keys():
            if prime in biggest_powers.keys():
                if prime_dict[prime] > biggest_powers[prime]:
                    biggest_powers[prime] = prime_dict[prime]
            else:
                biggest_powers[prime] = prime_dict[prime]

    product = 1
    for biggest in biggest_powers.keys():
        product *= biggest ** biggest_powers[biggest]
    return product


def prime_factorize(num):
    modify_this = num
    primes_used = []
    curr_prime = 2
    primes_powers = {}
    while modify_this != 1:
        if modify_this % curr_prime == 0:
            if curr_prime in primes_powers.keys():
                primes_powers[curr_prime] += 1
            else:
                primes_powers[curr_prime] = 1
            modify_this /= curr_prime
        else:
            primes_used.append(curr_prime)
            curr_prime = get_next_prime(curr_prime, primes_used)
    return primes_powers


def get_next_prime(curr_prime, primes_used):
    prime = curr_prime + 1
    divisible = False
    while not divisible:
        for num in primes_used:
            if prime % num == 0:
                divisible = True
        if divisible:
            prime += 1
            divisible = False
        return prime


if __name__ == "__main__":
    main()
