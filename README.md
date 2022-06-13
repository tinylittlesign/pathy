### Pathy 

A small example of a breadth-first approach to finding paths from a point to an exit in a space (because an acquintance was asking about it and I was bored). 
Also an excuse to get familiar with python's `curses` module. 
This is by no means a beautifully written piece of code, it's just a for funsies project thrown together in an hour or two.

To run, execute `curses.py` in an appropriate terminal emulator. 
Usage is as indicated by the the interface at the bottom: 

* Move the cursor with the arrow keys. 
* Press <kbd>w</kbd> to place a wall.
* Press <kbd>e</kbd> to place an exit that people can leave through.
* Press <kbd>p</kbd> to place a person. 
* Press <kbd>c</kbd> to run the breadth-first search and calculate paths from exits outwards. (Easter egg: instead press <kbd>/</kbd> to see a cute (and massively slowed down) little animation of this process, spreading outwards from the exit(s); afterwards press <kbd>/</kbd> again to clear the shading, if you want.).
* Press <kbd>r</kbd> to make people go to the exit(s). 
* Press <kbd>m</kbd> to place random walls all over (because making manual walls can get tiring). 
* Press <kbd>q</kbd> to quit. 
