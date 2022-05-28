#!/usr/bin/python

import time
import random
import os

# Get terminal's own clear command
clear = lambda: os.system('clear')

# Time between prints
delay = 0.2

class cell():
    def __init__(self,
                 c = " ",
                 pos = 0,
                 move = [],
                 visited = False,
                 exit = False,
                 wall = False):
        self.c = c
        self.pos = pos
        self.move = set(move)
        self.visited = visited
        self.exit = exit
        self.wall = wall

def jump(fr, to):
    if not cells[to].exit:
        cells[to].c = cells[fr].c
    cells[fr].c = "·"

# Just for cute printing when flood filling
def inc(char):
    return chr(ord(char) + 1)

### Initialise and draw grid
height = 12
width = 40

n = height * width
cells = [cell(pos = i) for i in range(n)]

for i in range(width):
    cells[i].wall = True
    cells[i].c = "▓"
    cells[n-i-1].wall = True
    cells[n-i-1].c = "▓"

for i in range(width-5):
    cells[width*6-i-1].wall = True
    cells[width*6-i-1].c = "▓"

for i in range(width-5):
    cells[width*8+i].wall = True
    cells[width*8+i].c = "▓"

for i in range(height):
    cells[width*i].wall = True
    cells[width*i].c = "▓"
    cells[width*(i + 1) - 1].wall = True
    cells[width*(i + 1) - 1].c = "▓"

def draw():
    clear()
    for i in range(n):
        if not i % width:
            print()
        print(cells[i].c, end="")
    print()

# Compute valid neighbour indices
def nbrs(i):
    nbrs = [i-width, i-1, i+1, i+width]
    if not i % width:
        nbrs.remove(i-1)
    if not (i + 1) % width:
        nbrs.remove(i+1)
    nbrs = list(filter(lambda j: 0 <= j < n, nbrs))
    nbrs = list(filter(lambda j: not cells[j].wall, nbrs))
    return nbrs

# Define exit cells
# exits = set([18, 70, 160])
exits = set([70])
for i in exits:
    cells[i].exit = True
    cells[i].visited = True
    cells[i].c = "⭘"

# Annotate each cell with neighbours that are closest to exit(s)
active = exits
t = 'a'
steps = 0

while True:
    new = set()
    for i in active:
        for j in nbrs(i):
            if not cells[j].visited:
                cells[j].move.add(i)
                # cells[j].c = t
                new.add(j)

    # draw()
    if not new:
        break

    for i in active:
        for j in nbrs(i):
            cells[j].visited = True
    active = new
    # t = inc(t)
    # time.sleep(delay)
    steps += 1

print("Charted optimal paths in", steps)


draw()

time.sleep(delay)

now = 420

cells[now].c = "•"

draw()

time.sleep(delay)

while (now not in exits):
    then = random.choice(list(cells[now].move))
    jump(now, then)
    now = then
    draw()
    time.sleep(delay)


# for c in cells:
#     print(c.move)
#
# print(cells[65].move)


# for i in range(height+2):
#     for j in range(width+2):
#         if i == 0:
#             if j == 0:
#                 print("╔", end="")
#             elif j == width+1:
#                 print("╗", end="")
#             else:
#                 print("═", end="")
#         elif i == height+1:
#             if j == 0:
#                 print("╚", end="")
#             elif j == width+1:
#                 print("╝", end="")
#             else:
#                 print("═", end="")
#         else:
#             if j == 0:
#                 print("║", end="")
#             elif j == width+1:
#                 print("║", end="")
#             else:
#                 print(" ", end="")
#     print()

"·•⭕"
