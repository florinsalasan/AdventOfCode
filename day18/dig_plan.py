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
    new_curr = curr_up_down - count
    return new_curr


def draw_down(count, curr_up_down):
    new_curr = curr_up_down + count
    return new_curr


def draw_left(count, curr_left_right):
    new_curr = curr_left_right - count
    return new_curr


def draw_right(count, curr_left_right):
    new_curr = curr_left_right + count
    return new_curr


for line in lines:
    dir, count, colour = line.split(' ')
    count = int(count)
    dir = dir.lower()
    print(max_down)
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

WIDTH = abs(max_right - max_left) + 1
HEIGHT = abs(max_down - max_up) + 1

print(WIDTH, HEIGHT)

# create the grid, and a path like we've done before, then count enclosed
# spaces like we've also done before

# If you start the path at -max_left, -max_right, should all fit in a grid
# of WIDTH, HEIGHT as defined above.


grid = []
for i in range(HEIGHT):
    grid.append(list('.' * WIDTH))

curr_left_right = -max_left
curr_up_down = -max_up

for list_item in grid:
    print(list_item)

for line in lines:
    dir, count, colour = line.split(' ')
    count = int(count)
    dir = dir.lower()

    print(curr_left_right, curr_up_down, dir)
    if dir == 'u':
        new_curr = draw_up(count, curr_up_down)
        print('new_curr: ' + str(new_curr))
        while curr_up_down != new_curr:
            grid[curr_up_down][curr_left_right] = '#'
            print('curr_ud: ' + str(curr_up_down))
            curr_up_down -= 1

    elif dir == 'd':
        new_curr = draw_down(count, curr_up_down)
        print('new_curr: ' + str(new_curr))
        while curr_up_down != new_curr:
            grid[curr_up_down][curr_left_right] = '#'
            print('curr_ud: ' + str(curr_up_down))
            curr_up_down += 1

    elif dir == 'r':
        new_curr = draw_right(count, curr_left_right)
        print('new_curr: ' + str(new_curr))
        while curr_left_right != new_curr:
            grid[curr_up_down][curr_left_right] = '#'
            print('curr_lr: ' + str(curr_left_right))
            curr_left_right += 1

    elif dir == 'l':
        new_curr = draw_left(count, curr_left_right)
        print('new_curr: ' + str(new_curr))
        while curr_left_right != new_curr:
            grid[curr_up_down][curr_left_right] = '#'
            print('curr_lr: ' + str(curr_left_right))
            curr_left_right -= 1

    for item in grid:
        print(item)

# Outline of the trench should be made in the grid at this point. Need to
# dig out the interior now, by that i mean just get the distance between
# '#' in each line other than the top and bottom which should be a straight
# line. In this approach I'm making a big assumption that it's not like day10
# where the grid can be very complex and 'fold' multiple times on the edges.
# This is very likely a stupidly naive approach that will back fire but I want
# to try for at least part1 anyways.

count = 0

for idx, line in enumerate(grid):
    if idx == 0 or idx == len(grid) - 1:
        count += line.count('#')
        print('first or last')
        print(count)
    else:
        stringified = ''.join(line)
        first_idx = stringified.find('#')
        second_idx = stringified.find('#', first_idx + 1)
        while stringified.find('#', second_idx + 1) != -1:
            second_idx = stringified.find('#', second_idx + 1)
        count += second_idx - first_idx + 1
        print('middle')
        print(second_idx, first_idx)
        print(count)

print(count)
