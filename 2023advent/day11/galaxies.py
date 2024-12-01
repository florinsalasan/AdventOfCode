import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python galaxies.py input.txt')

    with open(sys.argv[1]) as file_open:
        lines = file_open.readlines()

    if lines[-1] == '\n':
        lines = lines[:-1]

    # need to take in the input and then see which lines
    # do not contain '#' these need to be duplicated and
    # inserted below the line where there is only '.'
    galaxies = []
    for line in lines:
        curr_line = list(line)
        curr_line = curr_line[:-1]
        if '#' not in curr_line:
            # Need to make a copy otherwise inserting into
            # each line at different line_idx modifies both
            # resulting in those lines being longer than expected
            doubled_line = curr_line.copy()
            galaxies.append(doubled_line)
            galaxies.append(curr_line)
        else:
            galaxies.append(curr_line)

    columns_to_expand = []

    for column_idx in range(len(galaxies[0])):
        empty = True
        for line in galaxies:
            if line[column_idx] == '#':
                empty = False
        if empty:
            columns_to_expand.append(column_idx)

    print(columns_to_expand)
    for col_idx, col in enumerate(columns_to_expand):
        for line_idx, line in enumerate(galaxies):
            galaxies[line_idx].insert(col_idx + col, '.')

    # at this point the galaxies arrays have been properly
    # expanded, now need to find shortest path for each pair,
    # order doesn't matter so only count [1, 3] and [3, 1] once
    # will collect the galaxy coords after looping through
    # galaxy again, maybe give them numbers, idk
    galaxy_coords = []
    # coords will be [char_idx, line_idx] which is [x, y]

    for line_idx, line in enumerate(galaxies):
        for char_idx, char in enumerate(line):
            if char == '#':
                galaxy_coords.append([char_idx, line_idx])

    print(galaxy_coords)

    sum = 0
    count = 0
    for coord_idx, coord in enumerate(galaxy_coords):
        for i in range(coord_idx + 1, len(galaxy_coords), 1):
            count += 1
            print(coord_idx, i)
            # since you can't move diagonally in this case, dist
            # is sum of diffx and diffy
            if not (i) < len(galaxy_coords):
                print('breaks @: ')
                print(coord_idx, i)
                break
            curr_diff = (abs(galaxy_coords[coord_idx][0] - galaxy_coords[i][0]) +
                         abs(galaxy_coords[coord_idx][1] - galaxy_coords[i][1]))
            sum += curr_diff

    for line in galaxies:
        print(line)

    print(sum)


if __name__ == "__main__":
    main()
