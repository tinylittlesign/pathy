#!/usr/bin/python
import time
import random
import curses
from curses import wrapper

WALL = "▓"
PERSON = "•"
EXIT = "⭘"
EMPTY = " "
TRAIL = "·"

DELAY = 0.15

class cell():
    def __init__(self,
                 c = EMPTY,
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

    def make_wall(self):
        self.wall = True
        self.c = WALL
    def dest_wall(self):
        self.wall = False
        self.c = EMPTY
    def togg_wall(self):
        self.dest_wall() if self.wall else self.make_wall()

    def togg_pers(self):
        self.c = PERSON if self.c != PERSON else EMPTY

    def make_exit(self):
        self.exit = True
        self.c = EXIT
    def dest_exit(self):
        self.exit = False
        self.c = EMPTY
    def togg_exit(self):
        self.dest_exit() if self.exit else self.make_exit()


class grid():
    def __init__(self,
                 height = 10,
                 width = 10):
        self.height = height
        self.width = width
        self.n = self.height * self.width
        self.cells = [cell(pos = i) for i in range(self.n)]
        for i in range(self.width):
            self.cells[i].make_wall()
            self.cells[self.n-i-1].make_wall()
        for i in range(self.height):
            self.cells[self.width*i].make_wall()
            self.cells[self.width*(i + 1) - 1].make_wall()
    def draw(self, area, clear = False):
        area.erase()
        for i in range(self.n):
            if clear and self.cells[i].c == TRAIL:
                self.cells[i].c = EMPTY
            y = i // self.width
            x = i % self.width
            area.delch(y, x)
            area.insstr(y, x, self.cells[i].c)
        area.refresh()
    def jump(self, fr, to):
        if not self.cells[to].exit:
            self.cells[to].c = self.cells[fr].c
        self.cells[fr].c = TRAIL
    def nbrs(self, i):
        nbrs = [i-self.width, i-1, i+1, i+self.width]
        if not i % self.width:
            nbrs.remove(i-1)
        if not (i + 1) % self.width:
            nbrs.remove(i+1)
        nbrs = list(filter(lambda j: 0 <= j < self.n, nbrs))
        nbrs = list(filter(lambda j: not self.cells[j].wall, nbrs))
        return nbrs
    def path(self, recalculate=False):
        active = set(filter(lambda i: self.cells[i].exit, range(self.n)))
        if recalculate:
            for c in self.cells:
                c.move = set()
                c.visited = False
        steps = 0
        while True:
            new = set()
            for i in active:
                for j in self.nbrs(i):
                    if not self.cells[j].visited:
                        self.cells[j].move.add(i)
                        # cells[j].c = t
                        new.add(j)

            # draw()
            if not new:
                break

            for i in active:
                for j in self.nbrs(i):
                    self.cells[j].visited = True
            active = new
            # t = inc(t)
            # time.sleep(delay)
            steps += 1
    def animate(self, area):
        self.draw(area, clear=True)
        now = list(filter(lambda i: self.cells[i].c == PERSON, range(self.n)))
        exits = set(filter(lambda i: self.cells[i].exit, range(self.n)))
        while (now):
            new = []
            for p in now:
                i = p
                then = random.choice(list(self.cells[i].move))
                self.jump(i, then)
                i = then
                if not self.cells[i].exit:
                    new.append(i)
            now = new

            self.draw(area)
            time.sleep(DELAY)


def main(scr):
    rows, cols = scr.getmaxyx()
    # frame = curses.newwin(rows-4, cols)
    # frame.border()
    # frame.refresh()
    area = curses.newwin(rows-4, cols, 0, 0)
    tools = curses.newwin(4, cols, rows-4, 0)

    tools.addstr(1, 1, "Use arrow keys to navigate")
    tools.addstr(2, 1, "w - walls      e - exit      p - people")
    tools.border()
    tools.refresh()

    curses.setsyx(0, 0)
    y, x = curses.getsyx()
    maxy, maxx = area.getmaxyx()
    gr = grid(width = maxx, height = maxy)
    gr.draw(area)
    calc = 0
    while (True):
        p = y*maxx + x
        k = area.getch()
        match k:
            case 65: # Up
                y -= 1 if y > 0 else 0
            case 66: # Down
                y += 1 if y < maxy-1 else 0
            case 67: # Right
                x += 1 if x < maxx-1 else 0
            case 68: # Left
                x -= 1 if x > 0 else 0
            case 119: # w
                gr.cells[p].togg_wall()
                area.delch(y, x)
                area.insstr(y, x, gr.cells[p].c)
            case 112: # p
                gr.cells[p].togg_pers()
                area.delch(y, x)
                area.insstr(y, x, gr.cells[p].c)
            case 101: # e
                gr.cells[p].togg_exit()
                area.delch(y, x)
                area.insstr(y, x, gr.cells[p].c)
            case 99: # c
                gr.path(recalculate = calc > 0)
                calc += 1
            case 114: # r
                gr.animate(area)
            case 100: # d
                tools.addstr(1, 20, str(gr.cells[p].move))
                tools.addstr(1, 40, str(gr.cells[p].pos))
                tools.refresh()
            case 113: # q
                break
        area.move(y, x)

wrapper(main)
