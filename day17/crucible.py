# Looked at David Brownman's writeup of his solution and explanation to
# come up with my solution, was nice to know that Dijkstra's was a good
# path to start on, I just couldn't figure out the constraint of number of
# tiles in a row for a given direction. For the full write up see:
# https://advent-of-code.xavd.id/writeups/2023/day/17/

from enum import IntEnum
import sys
import heapq

Rotation = ['CCW', 'CW']

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


_OFFSETS = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, -1),
    Direction.LEFT: (-1, 0)
}

State = tuple[int, tuple[int, int], int]
