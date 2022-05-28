WALL = "▓"
PERSON = "•"
EXIT = "⭘"
EMPTY = " "
TRAIL = "·"

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
