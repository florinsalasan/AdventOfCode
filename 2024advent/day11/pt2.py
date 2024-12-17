import sys
from functools import lru_cache

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 pt1.py puzzle_input.txt')
with open(sys.argv[1]) as open_file:
    read_line = open_file.readlines()

str_line = read_line[0].split("\n")[0]
line = str_line.split(" ")
stones = []
for value in line:
    stones.append(int(value))

NUM_BLINKS = 75


def count_digit_len_no_typing(num):
    total = 0
    while num > 0:
        total += 1
        num = num // 10
    return total


@lru_cache(maxsize=None)
def expand_stone(stone, depth=0):
    while depth < NUM_BLINKS:
        print(depth)
        if stone == 0:
            stone = 1
            depth += 1
            continue

        digits = count_digit_len_no_typing(stone)
        if digits % 2 == 0:
            # if the length of the value engraved on the stone is even split it
            # into 2, removing leading zeros from the second stone
            mask = 10 ** (digits // 2)
            left_stone, right_stone = stone // mask, stone % mask
            # print(str1, str2, str_stone)
            return (expand_stone(left_stone, depth + 1) +
                    expand_stone(right_stone, depth + 1))

        stone *= 2024
        depth += 1

    # This counts the number of stones that will be collected by the end of
    # reaching all of the blinks
    return 1


print(sum(expand_stone(int(stone)) for stone in line))
