# Imports
import os, sys

# Program

# Check for root, not universal but it works
if os.geteuid() != 0:
    print >> sys.stderr, "This tool requires root"
    sys.exit()

# The interface
def interface():
   



# Begin the program
