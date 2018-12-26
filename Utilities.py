# utilities used in the interface and netork programs

# Imports
try:
    import os, sys
    from termcolor import cprint
    import curses
    from curses import wrapper # stops weird glitches
except ImportError as IE:
    print("an error importing has occured. {}".format(IE))
except Exception as E:
    print("error: {} has occured".format(E))
    sys.exit(1)

# actual code

# start the curses screen handling
# https://docs.python.org/3/howto/curses.html
def startScreen():
    # create a screen obj, turn on cbreak, enable specil handlers for keypad
    screen = curses.initscr()
    curses.cbreak()
    screen.keypad(True)
    return screen # return the screen
  #
def endScreen():
    # return everything to normal
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
  #
def drawWin(h, w, x, y):
    # create a new window oject of the specified h(eight), w(idth), begin y, and begin x
    return curses.newwin(h, w, y, x)
  #
