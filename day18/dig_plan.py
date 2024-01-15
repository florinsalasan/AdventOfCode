import sys

if len(sys.argv) != 2:
    sys.exit('Usage: python dig_plan.py input.txt')

with open(sys.argv[1]) as input_file:
    lines = input_file.readlines()

if lines[-1] == '' or lines[-1] == '\n':
    lines = lines[:-1]

print(lines)

max_up = 0
curr_up = 0
max_down = 0
curr_down = 0
max_left = 0
curr_left = 0
max_right = 0
curr_right = 0
