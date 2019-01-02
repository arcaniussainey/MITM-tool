#!/usr/local/bin
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
R, G, Y, B, P, LB, Grey, E = '\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[37m', '\033[0;0m'
PctCnt = 0; # the packet count
nps = nmap.PortScanner() # the port scanner

# packet parsers
def PathP(packet):
    # gets the packets src and destination
    PctCnt += 1
    print(f"Packet #{PctCnt} @{packet[0][1].src} ―→ {packet[0][1].dst} ")
    #
def PacketPrint(in):
    # colors a packet
    # how will this work with curses ?
    cprint(str(in), 'blue', attrs=["bold"]) # print in blue
  #
# settings

# scanner types
  # the target is the ip, the ports are the range of ports as such 34-40, or 22-181
def individualScan(targ, ports):
    nps.scan(str(targ), str(ports))
    # get the state of the targeted device, the open ports, vendor, etc
    PD = """"""
    for host in nps.all_hosts():
        PD += f"""
|-------------{R}Host:{E} {B}{host}@{nps[host].hostname()}{E}-------------|
| {R}Mac ADDR:{E} {B}nps[host]['addresses']['mac']{E}
| {R}IPv4:{E} {B}nps[host]['addresses']['ipv4']{E}
| {R}VENDOR:{E} {B}nps[host]['vendor'][nps[host]['addresses']['mac']]{E}
| {R}STATE:{E} {B}nps[host]['status']['mac']{E}
                """)
        for prot in nps[host].all_protocols():
            PD += f"""
|----------Protocals--------
PROTOCOL: {prot}
            """
            # after adding the protocol, it adds ports on the protocol
            lport = nps[host][prot].keys()
            lport.sort()
            for port in lport: # loop ports
                PD += f"""
|=-- PORT: {port} | STATE: {nps[host][prot][port]['state']}
                """ # print port and state
            # exiting third loop
        # exiting second loop
    # in function definition
    print(PD) # testing purposes, PD would be returned to the curses menu

  #
def CheckDeviceOnline(subnet):
    OnlineD = """\n===|: Online Devices :|===\n""" # doesnt handle not getting anything back
    nps.scan(arguments=f'-sP {subnet} --exclude 127.0.0.1') # scans given devices, such as 192.68.6.* or 10.0.0.0/14
    for host in nps.all_hosts(): # loop through scanned addresses
        if 'mac' in nps[host]['addresses']: # if there is a mac address then print it
            OnlineD += f""" Device: {G}{nps[host]['addresses']['mac']}{E} : {R}{nps[host]['status']['state']}{E} \n""" # get a devices mac, and state and show them
        else if 'ipv4' in nps[host]['addresses']: # if there is an ip, print it
            OnlineD += f""" Device: {G}{nps[host]['addresses']['1pv4']}{E} : {R}{nps[host]['status']['state']}{E} \n""" # get a devices ipv4, and state and show them
        else: # if there is neither, say unknown
            OnlineD += f""" Device: {G}Unknown{E} : {R}{nps[host]['status']['state']}{E} \n""" # get a devices mac, and state and show them
    return(OnlineD) # returns the devices and statuses
# sniffer types
  #
def RawSniff(f=""):
    # sniff the packet data, and return it raw to the console
    # add optional filters
    sniff(filter=str(f), prn=PacketPrint)# why someone would do this to themselfes is beyond me. JK.
  #
def PacketTrace(f=""):
    # sniff using the packet address filter
    sniff(filter="f", prn=PathP);
  #


NmapPD = """
{
	'hostnames':
		 [
			{'name': '',
			 'type': ''
			}
		 ],
	 'addresses':
		{
			'ipv4': '192.168.0.1',
			 'mac': '2C:7E:81:80:BC:51'
		},
	 'vendor':
		{
			'2C:7E:81:80:BC:51': 'Arris Group'
		},
	 'status':
		{
			'state': 'up',
			 'reason': 'arp-response'
		},
	 'tcp':
		{
			80:
				{
					'state': 'open',
					'reason': 'syn-ack',
					'name': 'tcpwrapped',
					'product': '',
					'version': '',
					'extrainfo': '',
					'conf': '8',
					'cpe': ''
				},
			1900:
				{
					'state': 'open',
					'reason': 'syn-ack',
					'name': 'http',
					'product': 'Cisco DPC3828S WiFi cable modem',
					'version': '',
					'extrainfo': '',
					'conf': '10',
					'cpe': 'cpe:/h:cisco:dpc3828s'
				},
			8080:
				{
					'state': 'open',
					'reason': 'syn-ack',
					'name': 'http',
					'product': 'Mongoose httpd',
					'version': '',
					'extrainfo': '',
					'conf': '10',
					'cpe': 'cpe:/a:cesanta:mongoose'
				}
		}
}
"""
