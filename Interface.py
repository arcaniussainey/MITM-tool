# Imports
import os, sys

# the banner
banner = 
"""


"""

# Program



# Check for root, not universal but it works
if os.geteuid() != 0:
    print >> sys.stderr, "This tool requires root"
    sys.exit()

# The interface
def interface():
    # Get input from the command line
    cmnd = str(input("\033[0;31m MITM:>\033[0;0m"));
    print(cmnd) # testing

interface() # for testing purposes

def start():
    try:
        print(banner)
        # Infinite loop
        while True:
            # things that need to happen for the program to start
            interface()
    except:
        sys.exit()
# Begin the program
# start()
