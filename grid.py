from cell import cell
import random
import time

WALL = "▓"
PERSON = "•"
EXIT = "⭘"
EMPTY = " "
TRAIL = "·"

class grid():
    def __init__(self,
                 height = 10,
                 width = 10,
                 DELAY = 0.2):
        self.height = height
        self.width = width
        self.n = self.height * self.width
        self.DELAY = DELAY
        self.clear()
        # Always initialist walls around the grid
        # for i in range(self.width):
        #     self.cells[i].make_wall()
        #     self.cells[self.n-i-1].make_wall()
        # for i in range(self.height):
        #     self.cells[self.width*i].make_wall()
        #     self.cells[self.width*(i + 1) - 1].make_wall()

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
    def path(self, recalculate=False, fill=False, area=False, curses=False):
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
                        new.add(j)
                        if fill:
                            y = j // self.width
                            x = j % self.width
                            area.delch(y, x)
                            area.insstr(y, x, "▒") #▒░
                            area.refresh()
            if not new:
                break

            for i in active:
                for j in self.nbrs(i):
                    self.cells[j].visited = True
            active = new
            if fill:
                time.sleep(self.DELAY/2)
            steps += 1
    def animate(self, area):
        self.draw(area, clear=True)
        now = list(filter(lambda i: self.cells[i].c == PERSON, range(self.n)))
        exits = set(filter(lambda i: self.cells[i].exit, range(self.n)))
        while (now):
            new = []
            for p in now:
                i = p
                move = list(self.cells[i].move)
                if move:
                    then = random.choice(move)
                else:
                    continue
                self.jump(i, then)
                i = then
                if not self.cells[i].exit:
                    new.append(i)
            now = new

            self.draw(area)
            time.sleep(self.DELAY)
    def clear(self):
        self.cells = [cell(pos = i) for i in range(self.n)]
    def maze(self, area):
        self.clear()
        for c in self.cells:
            r = random.random()
            if r < 0.25:
                c.make_wall()
        self.draw(area, clear=True)
