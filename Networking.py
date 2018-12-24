# imports
try:
    from __future__ import print_function #python 2? idk why i added this but its staying
    import os, sys
    from termcolor import cprint
    import platform
    from scapy.all import * # optomise later
    import nmap
except:
    print("There was a problem importing packages, make sure the requirements are installed", file=sys.stderr)
    sys.exit()
# actual code
PctCnt = 0;
nps = nmap.PortScanner()

# packet parsers
def AddrP(packet):
    PctCnt += 1
    print(f"Packet #{PctCnt} @{packet[0][1].src} ==> {packet[0][1].dst} ")
  #
def PacketPrint(in):
    cprint(str(in), 'blue', attrs=["bold"]) # print in blue
  #
# settings

# scanner types
def individualScan(targ, ports):
    ScanData = nps.scan(str(targ), str(ports))
# sniffer types
  #
def RawSniff(f=""):
    # sniff the packet data, and return it raw to the console
    # add optional filters
    sniff(filter=str(f), prn=PacketPrint)# why someone would do this to themselfes is beyond me. JK.
  #
def PacketTrace(f=""):
    # sniff using the packet address filter
    sniff(filter="f", prn=AddrP);
  #
def Nuke(f=""):
    NukeMessage = "☢ Doom is incoming ☢"
