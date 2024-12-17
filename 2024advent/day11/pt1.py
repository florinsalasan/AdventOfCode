import sys

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 pt1.py puzzle_input.txt')
with open(sys.argv[1]) as open_file:
    read_line = open_file.readlines()

str_line = read_line[0].split("\n")[0]
line = str_line.split(" ")

NUM_BLINKS = 25


# pass in the int value of the stone
def modify_stones(stone):
    # Go through the list of rules to modify the current stone
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        # if the length of the value engraved on the stone is even split it
        # into 2, removing leading zeros from the second stone
        str_stone = str(stone)
        str1, str2 = str_stone[:len(str_stone)//2], str_stone[len(str_stone)//2:]
        print(str1, str2, str_stone)
        return [int(str1), int(str2)]
    else:
        new_val = stone * 2024
        return [new_val]


stones = line
for blink in range(NUM_BLINKS):
    collected = []
    for stone in stones:
        int_stone = int(stone)
        collected += modify_stones(int_stone)
    stones = collected
    print(len(collected))
