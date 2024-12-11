import sys

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 pt1.py puzzle_input.txt')
with open(sys.argv[1]) as open_file:
    lines = open_file.readlines()

WIDTH = len(lines[0]) - 1
HEIGHT = len(lines)

antenna_and_their_positions = {}
# iterate over grid to collect the different antenna frequencies and their
# positions in the grid
for y_idx, line in enumerate(lines):
    for x_idx, value in enumerate(line):
        if value != "." and value != "\n":
            if value in antenna_and_their_positions:
                antenna_and_their_positions[value].append((x_idx, y_idx))
            else:
                antenna_and_their_positions[value] = [(x_idx, y_idx)]
