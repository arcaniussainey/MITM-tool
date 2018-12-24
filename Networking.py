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
def PathP(packet):
    # gets the packets src and destination
    PctCnt += 1
    print(f"Packet #{PctCnt} @{packet[0][1].src} ―→ {packet[0][1].dst} ")
  #
def PacketPrint(in):
    # colors a packet
    cprint(str(in), 'blue', attrs=["bold"]) # print in blue
  #
# settings

# scanner types
  # the target is the ip, the ports are the range of ports as such 34-40, or 22-181
def individualScan(targ, ports):
    SD = nps.scan(str(targ), str(ports))
    # get the state of the targeted device, the open ports, vendor, etc
    state = SD['scan']['']
    return """


           """
  #
def CheckOnline():
    nps.scan(arguments='-pn')
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
