import sys

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 pt1.py puzzle_input.txt')
with open(sys.argv[1]) as open_file:
    lines = open_file.readlines()

LINES = lines

HEIGHT = len(lines)
WIDTH = len(lines[0])

WORD = 'MAS'


def main():

    num_xmas = 0
    for y_idx, line in enumerate(LINES):
        for x_idx, char in enumerate(line):
            if char == 'A':
                num_xmas += is_x_mas(x_idx, y_idx)

    print(num_xmas)
    return num_xmas


def is_x_mas(x_idx, y_idx):
    if y_idx == 0 or x_idx == 0 or y_idx == HEIGHT - 1 or x_idx == WIDTH - 1:
        return 0
    # Checked if along an edge since cannot make an 'X' form in this case
    # so now get the values in each corner around the 'A'
    top_right = LINES[y_idx - 1][x_idx + 1]
    top_left = LINES[y_idx - 1][x_idx - 1]
    bottom_right = LINES[y_idx + 1][x_idx + 1]
    bottom_left = LINES[y_idx + 1][x_idx - 1]

    if not (bottom_left == 'M' or bottom_left == 'S'):
        return 0
    if not (bottom_right == 'M' or bottom_right == 'S'):
        return 0
    if not (top_right == 'M' or top_right == 'S'):
        return 0
    if not (top_left == 'M' or top_left == 'S'):
        return 0

    # Check across diagonals for 'MAS' formed twice
    if not ((bottom_left == 'M' and top_right == 'S') or
            (bottom_left == 'S' and top_right == 'M')):
        return 0
    if not ((bottom_right == 'M' and top_left == 'S') or
            (bottom_right == 'S' and top_left == 'M')):
        return 0

    return 1


if __name__ == '__main__':
    main()
