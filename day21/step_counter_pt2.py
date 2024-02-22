'''
Turns out we need far more steps, going from 64 -> 26501365, which makes 
the search space far larger than what we had before which was already mind
boggling. So we now need a way to solve this in a smart way rather than just 
finding a way to avoid backtracking. The garden input also expands infinitely
in each direction, repeating the same garden kind of like tile pieces coming
together. What we do know is that at most we can reach 26501365 steps away in
a direct line north, south, east, or west if there are no walls in the way.
But there are so the actual area would be smaller. Then the 4 points that can
be reached by only going NSEW, would be connected in roughly straight lines
forming a jagged diamond as possible end points for the steps.

That's great and everything but I'm unsure of how to begin to implement this
so I'll scale it down, assume we have two steps to move from the start for 
the 5x5 grid, for the 8x8 grid use 5 steps for final position

.....                   . . . . . . . .
.....                   . # . . . # . .
..S..                   . . . . . . . .
.....                   . . . . . . # .
.....                   . . . # S . . .
  |                     . . . . . . . .
  |                     . # . # . . # .
  |                     . . . . . . . .
  V
..o..                   . . . o . o . .
.o.o.                   . # . . . # o .
o.S.o                   . . . . . . . o
.o.o.                   o . . . . . # .
..o..                   . o . # S . . .
                        o . . . . . . .
                        . # . # . . # o
                        . . . . . . o .

diamond shaped is formed, roughly
'''

