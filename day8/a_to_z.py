import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python a_to_z.py puzzle_input.txt')

    with open(sys.argv[1]) as input_file:
        lines = input_file.readlines()

    path = lines[0]
    path = path[:-1]

    node_to_nodes = {}
    rl_to_idx = {
        'L': 0,
        'R': 1,
    }
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

    found = False
    i = 0
    count = 0
    curr_node = 'AAA'
    while not found:
        curr_node = node_to_nodes[curr_node][rl_to_idx[path[i]]]
        count += 1
        if curr_node == 'ZZZ':
            found = True
        else:
            i = (i + 1) % (len(path))

    print(count)
    return count


if __name__ == "__main__":
    main()
