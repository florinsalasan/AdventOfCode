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

    pipe_loop = [pipe_loop[-1]] + pipe_loop[:-1]

    # for test_input.txt, the only enclosed tile should be at [2, 2] i think
    # currently I have an issue, when I get test_enclosed working, test_enclosed2
    # no longer works, and vice versa, need to find a better way of counting walls
    # whether a node is contained inside based on that or not.
    enclosed = []
    for y_idx, line_at_y in enumerate(maze):
        # if y_idx == 6:
        num_crossings = 0
        for x_idx, char in enumerate(line_at_y):
            if [x_idx, y_idx] in pipe_loop:
                # only check below for another wall:
                # print(x_idx, y_idx)
                if [x_idx, y_idx + 1] in pipe_loop:
                    # print(x_idx, y_idx + 1)
                    # check that diff in index is only one
                    curr_idx = pipe_loop.index([x_idx, y_idx])
                    below_idx = pipe_loop.index([x_idx, y_idx + 1])
                    diff = (curr_idx - below_idx)
                    # print(curr_idx, below_idx, diff)
                    if diff == 1:
                        num_crossings += 1
                    elif diff == -1:
                        num_crossings -= 1
                    # else:
                       # print('shouldnt see this')
                       # print(curr_idx, below_idx, diff)
            elif num_crossings == 1:
                enclosed.append([x_idx, y_idx])
    # print(enclosed, len(enclosed))
    print(len(enclosed))


def get_next_node(curr_node, directions, prev_node, maze):
    x, y = curr_node[0], curr_node[1]
    curr_node_symbol = maze[y][x]
    for direction in directions[curr_node_symbol]:
        if [x + direction[0], y + direction[1]] != prev_node:
            return [x + direction[0], y + direction[1]]
    # should never not return one of the two possible nodes
    print('Something went wrong, check helper')
    return -1


if __name__ == "__main__":
    main()
