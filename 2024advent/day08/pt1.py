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


def find_antinodes(antenna_and_their_positions):
    antinode_positions = set()
    # go through each frequency, find any valid antinode positions and throw
    # them into a set, return len of the set
    for freq in antenna_and_their_positions.keys():
        antennas = antenna_and_their_positions[freq]
        for i in range(len(antennas)):
            for j in range(i + 1, len(antennas)):
                diff_x = antennas[i][0] - antennas[j][0]
                diff_y = antennas[i][1] - antennas[j][1]
                
                if diff_y == 0:
                    print("same y_idx")
                if diff_x == 0:
                    print("same x_idx")

                behind_i_x = antennas[i][0] + diff_x
                behind_i_y = antennas[i][1] + diff_y

                ahead_j_x = antennas[j][0] - diff_x
                ahead_j_y = antennas[j][1] - diff_y

                if (behind_i_x >= 0 and behind_i_x < WIDTH and
                        behind_i_y >= 0 and behind_i_y < HEIGHT):
                    antinode_positions.add((behind_i_x, behind_i_y))

                if (ahead_j_x >= 0 and ahead_j_x < WIDTH and
                        ahead_j_y >= 0 and ahead_j_y < HEIGHT):
                    antinode_positions.add((ahead_j_x, ahead_j_y))

    for position in antinode_positions:
        print(position)

    print(len(antinode_positions))


find_antinodes(antenna_and_their_positions)
