# Imports
try:
    import os, sys
    from termcolor import cprint
    import curses
    from curses import wrapper
    # ^- used to rap curses program, such as wrapper(interface)
except ImportError as IE:
    print("an error importing has occured. {}".format(IE))
except Exception as E:
    print("error: {} has occured".format(E))
    sys.exit(1)
# the banner

#for cool ascii symbols checkout  https://coolsymbol.com/ or use alt + keypad keys
def Banner():
    cprint("""
  ================================================
    ➵   _     ➴            _    ➴   ➶         _
     ___| | __ _ _ __➴  __| | ___ _ __ ___ __| |
    / __| |/ _` | `_ \_/ _` |/ __\ '__/ _ \/ _` |
    \__ \ | (_| | | | | (_| |___/| |  __/ (_|  |
    |___/_|\__,_|_| |_|\__,_|\___|_|  \___|\__,_|
  =================================================

 """, 'red', attrs=['bold'])

banner_info = """
          Version: v.0.1
Made By: @Linux-fisher, ☢arcaniussainey


"""

# Program

# Check for root, not universal but it works
try:
    if os.geteuid() != 0:
        print("This tool requires root!!!", file=sys.stderr)
        sys.exit(1)
except:
    pass

# The interface
def interface():
    # Get input from the command line
    cmnd = input("\033[0;31m MITM:》\033[0;0m ");
    print(cmnd) # testing

interface() # for testing purposes

def start():
    try:
        try:
            os.system("clear");
        except: # is there a way to do this with sys, yes, will i, not now
            os.system("cls");
        except:
            pass
        # things that need to happen for the program to start
        Banner()
        # Infinite loop
        while True:
            interface()
    except KeyboardInterrupt as endkey:
        # do everything tht needs to be done to exit
        print("Program terminated")
        sys.exit()
    except Exception as e:
        print("Error {} has occured".format(e), file=sys.stderr)
        sys.exit()
# Begin the program

# start()
