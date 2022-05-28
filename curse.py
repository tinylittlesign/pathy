#!/usr/bin/python
import curses
from curses import wrapper

from grid import grid

WALL = "▓"
PERSON = "•"
EXIT = "⭘"
EMPTY = " "
TRAIL = "·"
DELAY = 0.15


def main(scr):
    rows, cols = scr.getmaxyx()
    area = curses.newwin(rows-5, cols, 0, 0)
    tools = curses.newwin(5, cols, rows-5, 0)

    tools.addstr(1, 1, "Use arrow keys to navigate")
    tools.addstr(2, 1, "w - wall          e - exit      p - people      ")
    tools.addstr(3, 1, "c - calc path     r - run       m - random walls")
    tools.border()
    tools.refresh()

    curses.setsyx(0, 0)
    y, x = curses.getsyx()
    maxy, maxx = area.getmaxyx()

    def warn(area):
        dialogue = curses.newwin(4, 26, maxy//2 - 2, maxx//2 - 13)
        dialogue.border()
        dialogue.addstr(1, 1, "Conditions have changed")
        dialogue.addstr(2, 1, "You must recalculate (c)")
        dialogue.overlay(area)
        dialogue.refresh()
        return dialogue

    dialogue = []

    gr = grid(width = maxx, height = maxy, DELAY = DELAY)
    gr.draw(area)
    recalculate = False
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
                recalculate = True
            case 112: # p
                gr.cells[p].togg_pers()
                area.delch(y, x)
                area.insstr(y, x, gr.cells[p].c)
            case 101: # e
                gr.cells[p].togg_exit()
                area.delch(y, x)
                area.insstr(y, x, gr.cells[p].c)
                recalculate = True
            case 99: # c
                if dialogue:
                    dialogue.clear()
                    dialogue.refresh()
                gr.draw(area)
                # area.refresh()
                gr.path(recalculate = recalculate)
                recalculate = False
            case 114: # r
                if recalculate:
                    dialogue = warn(area)
                else:
                    gr.animate(area)
            case 100: # d
                tools.addstr(1, 20, str(gr.cells[p].move))
                tools.addstr(1, 40, str(gr.cells[p].pos))
                tools.refresh()
            case 109: # m
                gr.maze(area)
                recalculate = True
            case 113: # q
                break
        area.move(y, x)

wrapper(main)
