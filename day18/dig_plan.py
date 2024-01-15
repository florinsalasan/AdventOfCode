import sys

if len(sys.argv) != 2:
    sys.exit('Usage: python dig_plan.py input.txt')

with open(sys.argv[1]) as input_file:
    lines = input_file.readlines()

if lines[-1] == '' or lines[-1] == '\n':
    lines = lines[:-1]

print(lines)

max_up = 0
max_down = 0
curr_up_down = 0
max_left = 0
max_right = 0
curr_left_right = 0


def move_up(count, curr_up_down):
    curr_up_down -= count
    return curr_up_down


def move_down(count, curr_up_down):
    curr_up_down += count
    return curr_up_down


def move_left(count, curr_left_right):
    curr_left_right -= count
    return curr_left_right


def move_right(count, curr_left_right):
    curr_left_right += count
    return curr_left_right


def draw_up(count, curr_up_down):
    new_curr = curr_up_down + count
    return new_curr


def draw_down(count, curr_up_down):
    new_curr = curr_up_down + count
    return new_curr


def draw_left(count, curr_left_right):
    new_curr = curr_left_right + count
    return new_curr


def draw_right(count, curr_left_right):
    new_curr = curr_left_right + count
    return new_curr


for line in lines:
    dir, count, colour = line.split(' ')
    count = int(count)
    dir = dir.lower()
    if dir == 'u':
        new_curr = move_up(count, curr_up_down)
        curr_up_down = new_curr
        if curr_up_down < max_up:
            max_up = curr_up_down

    elif dir == 'd':
        new_curr = move_down(count, curr_up_down)
        curr_up_down = new_curr
        if curr_up_down > max_down:
            max_down = curr_up_down

    elif dir == 'r':
        new_curr = move_right(count, curr_left_right)
        curr_left_right = new_curr
        if curr_left_right > max_right:
            max_right = curr_left_right

    elif dir == 'l':
        new_curr = move_left(count, curr_left_right)
        curr_left_right = new_curr
        if curr_left_right < max_left:
            max_left = curr_left_right

print(max_left, max_up, max_right, max_down)

WIDTH = abs(max_left - max_right)
HEIGHT = abs(max_up - max_down)

print(WIDTH, HEIGHT)

# create the grid, and a path like we've done before, then count enclosed
# spaces like we've also done before

# If you start the path at -max_left, -max_right, should all fit in a grid
# of WIDTH, HEIGHT as defined above.

grid = [list('.'*WIDTH)] * HEIGHT

curr_left_right = -max_left
curr_up_down = -max_up

for line in lines:
    dir, count, colour = line.split(' ')
    count = int(count)
    dir = dir.lower()

    if dir == 'u':
        new_curr = draw_up(count, curr_up_down)
        curr_up_down = new_curr
        if curr_up_down < max_up:
            max_up = curr_up_down

    elif dir == 'd':
        new_curr = draw_down(count, curr_up_down)
        curr_up_down = new_curr
        if curr_up_down > max_down:
            max_down = curr_up_down

    elif dir == 'r':
        new_curr = draw_right(count, curr_left_right)
        curr_left_right = new_curr
        if curr_left_right > max_right:
            max_right = curr_left_right

    elif dir == 'l':
        new_curr = draw_left(count, curr_left_right)
        curr_left_right = new_curr
        if curr_left_right < max_left:
            max_left = curr_left_right
