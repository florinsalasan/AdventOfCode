import sys


def main():
    # Want to find the number of tiles that are fully enclosed within the loop
    # for example:
    # .....
    # .F-7.
    # .|X|.
    # .|X|.
    # .L-J.
    # .....
    # only the spaces marked as 'X' would count towards the enclosed,
    # same with the maze below.
    # .......
    # ..F--7.
    # .FJXX|.
    # .|F--J.
    # .|L--7.
    # .L---J.
    # .......

    # To begin counting the enclosed spaces need to draw the path of the
    # maze, can use the part1 algo to get the entirety of the path then
    # there should be a way to determine which tiles are completely enclosed
    # in the loop

    if (len(sys.argv) != 2):
        sys.exit('Usage: python enclosed.py maze.txt')

    with open(sys.argv[1]) as maze_file:
        lines = maze_file.readlines()

    # Read in all of the lines from the file, remove the last line if it's
    # only a newline char and create a 2d array to then iterate over and
    # path through the types that I'll define in a dict.
    if lines[-1] == '\n':
        lines = lines[:-1]

    # Create the dict for what each character means. keys are the chars
    # found in the maze, the values are list of lists of length two that
    # are the modifiers for x and y indices when pathing
    directions = {
        '|': [[0, 1], [0, -1]],
        '-': [[1, 0], [-1, 0]],
        'L': [[0, -1], [1, 0]],
        'J': [[0, -1], [-1, 0]],
        '7': [[0, 1], [-1, 0]],
        'F': [[0, 1], [1, 0]],
        # 'S': [[1, 0]],
        '.': [[0, 0]],
        'S': [[1, 0], [-1, 0], [0, -1], [0, 1]]
    }
    starting_coords = []
    maze = []
    for line_idx, line in enumerate(lines):
        # do this to avoid having to clean up \n
        curr_line = list(line.split()[0])
        # print(curr_line)
        # The above print just recreates the maze, does not work for puzzle
        # input since it's too large but nice for the test inputs.
        if 'S' in curr_line:
            # x, y
            starting_coords = [curr_line.index('S'), line_idx]
        maze.append(curr_line)
    new_maze = []
    for yvalues in range(len(maze) + 1):
        new_maze.append(list('.'*len(maze[0])))

    # maze should be built now, and we should have the starting point from 'S'
    # now need to do traversal in every possible direction from 'S' and then
    # use the dictionary to traverse the sub directions using the values
    # should keep track of which nodes have already been visited to not
    # bounce back and forth forever and reach recursive limits. Ok the input
    # specifies that the pipe will always be a loop and each pipe will only
    # have two possible directions including the starting node. So will use
    # a while loop instead of doing this recursively. Stop the loop once
    # both of the traversals are at the same starting point.

    # Need to first determine which of the two directions the starting
    # position can travel to, not as easy as saying if it's not '.'
    # it can be traveled in that direction, instead need to check if
    # applying the directions from the dict to the node around the start
    # returns to the starting node, then can say pipe can go in that direction

    first_nodes = []
    for direction in directions['S']:
        valid = False
        # get the char at one of the 4 directions from 'S'
        # starting[0] is for x, direction[0] is for x so curr[0] is x,
        # maze is indexed as maze[y][x]
        curr_check = [starting_coords[0] + direction[0],
                      starting_coords[1] + direction[1]]
        for node_dir in directions[maze[curr_check[1]][curr_check[0]]]:

            if [curr_check[0] + node_dir[0], curr_check[1] + node_dir[1]] == starting_coords:
                valid = True
        if valid:
            first_nodes.append(
                [starting_coords[0] + direction[0], starting_coords[1] + direction[1]])

    # there should only be two nodes in first nodes
    prev_first = starting_coords
    first_path = first_nodes[0]
    pipe_loop = [first_path]
    while first_path != starting_coords:
        # find the correct direction to continue in for a path
        # by ensuring it doesn't return to the prev value, update
        # both curr path value and prev value
        temp_first = get_next_node(first_path, directions, prev_first, maze)
        prev_first = first_path
        first_path = temp_first
        pipe_loop.append(first_path)

    # pipe_loop should get all of the nodes coordinates for the loop, the
    # last coordinate in pipe_loop will be the starting coordinates.

    # now that we have the list of coords that make up the loop, I'd like
    # to try the ray cast method of determining whether a point is within
    # the loop, I may be implementing this horrifically incorrectly but
    # for each line I want to get the 'edges' of the pipe so to speak, there
    # should be an even number of these edges otherwise the loop wouldn't
    # be closed, then I want to sort by x coordinate to find the ranges
    # where there could be enclosed tiles. Should probably do this check
    # vertically and horizontally for every tile to check. but to begin
    # with I'll only do it in one direction to save some time.
    # should probably sort and split the path edges into lists for
    # each y_index
    for i, coords in enumerate(pipe_loop):
        for j in range(len(pipe_loop) - i - 1):
            # sort the coords by y index and subsort by x coords
            if pipe_loop[j][1] > pipe_loop[j + 1][1]:
                pipe_loop[j], pipe_loop[j + 1] = pipe_loop[j + 1], pipe_loop[j]
            elif pipe_loop[j][1] == pipe_loop[j + 1][1]:
                if pipe_loop[j][0] > pipe_loop[j + 1][0]:
                    pipe_loop[j], pipe_loop[j +
                                            1] = pipe_loop[j + 1], pipe_loop[j]

    # create the dict that contains all edges for a given y coordinate:
    edges_at_y = {}
    for coord in pipe_loop:
        if maze[coord[1]][coord[0]] == '7':
            new_maze[coord[1]][coord[0]] = '┐'
        elif maze[coord[1]][coord[0]] == 'J':
            new_maze[coord[1]][coord[0]] = '┘'
        elif maze[coord[1]][coord[0]] == 'F':
            new_maze[coord[1]][coord[0]] = '┌'
        elif maze[coord[1]][coord[0]] == 'L':
            new_maze[coord[1]][coord[0]] = '└'
        else:
            new_maze[coord[1]][coord[0]] = maze[coord[1]][coord[0]]
        if coord[1] in edges_at_y.keys():
            edges_at_y[coord[1]] += [coord]
        else:
            edges_at_y[coord[1]] = [coord]

    # for test_input.txt, the only enclosed tile should be at [2, 2] i think
    # currently I have an issue, when I get test_enclosed working, test_enclosed2
    # no longer works, and vice versa, need to find a better way of counting walls
    # whether a node is contained inside based on that or not.
    enclosed = []
    count = 0
    for y_idx, line, in enumerate(maze):
        if y_idx not in edges_at_y.keys():
            continue
        enclosed_inline = find_gaps(line, edges_at_y, y_idx)
        enclosed.append(enclosed_inline[1])
        count += enclosed_inline[0]

    for lineabc in new_maze:
        print(''.join(lineabc))

    print(count, enclosed)
    return count


def get_next_node(curr_node, directions, prev_node, maze):
    x, y = curr_node[0], curr_node[1]
    curr_node_symbol = maze[y][x]
    for direction in directions[curr_node_symbol]:
        if [x + direction[0], y + direction[1]] != prev_node:
            return [x + direction[0], y + direction[1]]
    # should never not return one of the two possible nodes
    print('Something went wrong, check helper')
    return -1


def find_gaps(line, edges, edge_key):
    # Reminder that the edges are pre sorted in main
    # if edge_key == 5:
    x_values = []
    count = 0
    tiles = []
    for value in edges[edge_key]:
        x_values.append(value[0])
    # we now have the x values for the line, group
    # them to create continuous walls, if there is an
    # even number of walls, can check between every pair,
    # ie if walls at [1, 3, 5, 7] we can say enclosed in
    # between 1 and 3 and between 5 and 7 so return x = 2, 6
    # for a count of 2.
    walls = []
    # want to group all values that are adjacent, so 1, 2, 4, 5
    # would become [[1,2], [4,5]]
    x = 0
    while x < len(x_values):
        wall = [x_values[x]]
        while (x + 1 < len(x_values) and x_values[x + 1] - 1 == x_values[x]):
            wall.append(x_values[x + 1])
            x += 1
        walls.append(wall)
        x += 1

    print(walls)
    # now have list of walls, if even find all values in between
    tiles = []
    walls_crossed = 0
    for i, wall in enumerate(walls):
        # find the number in between end of wall i and start of wall i + 1
        walls_crossed += 1
        if (walls_crossed) % 2 == 1:
            # try finding gap between curr wall and next
            if i + 1 < len(walls):
                start = walls[i][-1]
                end = walls[i + 1][0]
                count += end - start - 1
                for j in range(end - start - 1):
                    tiles.append([start + 1 + j, edge_key])

        # print(tiles)

    return [count, tiles]
    # return [0, []]


if __name__ == "__main__":
    main()
