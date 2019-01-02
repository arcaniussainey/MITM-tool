#!/usr/local/bin
# imports
try:
    from __future__ import print_function #python 2? idk why i added this but its staying
    import os, sys
    from termcolor import cprint
    import platform
    from scapy.all import * # optomise later
    import nmap
    import random
except:
    print("There was a problem importing packages, make sure the requirements are installed", file=sys.stderr)
    sys.exit()
# actual code
R, G, Y, B, P, LB, Grey, E = '\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[37m', '\033[0;0m'
global PctCnt = 0; # the packet count
nps = nmap.PortScanner() # the port scanner

# packet parsers
def PathP(packet):
    # gets the packets src and destination
    PctCnt += 1
    return(f"Packet #{PctCnt} @{packet[0][1].src} ―→ {packet[0][1].dst} ")
    #
def PacketPrint(in):
    # colors a packet
    # how will this work with curses ?
    return(f"{Y}{in}{E}") # return in blue, use RE to make urls awesome and red
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

# spoofer boiiiis
def randomMAC():
    return [ random.randint(0x5a, 0x9f), # random numbers between hex values, why? becuase numbers @r3n37 1337
        random.randint(0x07, 0x2f),
        random.randint(0x00, 0x6f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
  #
def MACprettyprint(mac):
    return ':'.join(map(lambda x: "%02x" % x, mac))


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

# below here is just example data for me to mess with, when i cant replicate
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
exampleP = """
ARP : <Ether  dst=33:33:00:00:00:01 src=2c:7e:81:80:bc:51 type=0x86dd |<IPv6  version=6 tc=0 fl=0 plen=120 nh=ICMPv6 hlim=255 src=fe80::2e7e:81ff:fe80:bc51 dst=ff02::1 |<ICMPv6ND_RA  type=Router Advertisement code=0 cksum=0xc7c chlim=64 M=1 O=1 H=0 prf=Medium (default) P=0 res=0 routerlifetime=1800 reachabletime=0 retranstimer=0 |<ICMPv6NDOptSrcLLAddr  type=1 len=1 lladdr=2c:7e:81:80:bc:51 |<ICMPv6NDOptPrefixInfo  type=3 len=4 prefixlen=64 L=1 A=1 R=0 res1=0 validlifetime=0x54600 preferredlifetime=0x54600 res2=0x0 prefix=2601:800:4000:8090:: |<ICMPv6NDOptRouteInfo  type=24 len=3 plen=60 res1=0 prf=0 res2=0 rtlifetime=257558 prefix=2601:800:4000:8090:: |<ICMPv6NDOptRDNSS  type=25 len=5 res=0 lifetime=60 dns=[ 2001:558:feed::1, 2001:558:feed::2 ] |>>>>>>>
=====
HTTP : <Ether  dst=ff:ff:ff:ff:ff:ff src=f0:6e:0b:82:08:e7 type=0x806 |<ARP  hwtype=0x1 ptype=0x800 hwlen=6 plen=4 op=who-has hwsrc=f0:6e:0b:82:08:e7 psrc=192.168.0.4 hwdst=00:00:00:00:00:00 pdst=192.168.0.29 |<Padding  load='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' |>>>
=====
UDP : <Ether  dst=ff:ff:ff:ff:ff:ff src=f0:6e:0b:82:08:e7 type=0x806 |<ARP  hwtype=0x1 ptype=0x800 hwlen=6 plen=4 op=who-has hwsrc=f0:6e:0b:82:08:e7 psrc=192.168.0.4 hwdst=00:00:00:00:00:00 pdst=192.168.0.29 |<Padding  load='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' |>>>
--------RAW--------
ARP : b'33\x00\x00\x00\x01,~\x81\x80\xbcQ\x86\xdd`\x00\x00\x00\x00x:\xff\xfe\x80\x00\x00\x00\x00\x00\x00.~\x81\xff\xfe\x80\xbcQ\xff\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x86\x00\x0c|@\xc0\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01,~\x81\x80\xbcQ\x03\x04@\xc0\x00\x05F\x00\x00\x05F\x00\x00\x00\x00\x00&\x01\x08\x00@\x00\x80\x90\x00\x00\x00\x00\x00\x00\x00\x00\x18\x03<\x00\x00\x03\xee\x16&\x01\x08\x00@\x00\x80\x90\x00\x00\x00\x00\x00\x00\x00\x00\x19\x05\x00\x00\x00\x00\x00< \x01\x05X\xfe\xed\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01 \x01\x05X\xfe\xed\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
=====
UDP : b'\xff\xff\xff\xff\xff\xff\xf0n\x0b\x82\x08\xe7\x08\x06\x00\x01\x08\x00\x06\x04\x00\x01\xf0n\x0b\x82\x08\xe7\xc0\xa8\x00\x04\x00\x00\x00\x00\x00\x00\xc0\xa8\x00\x1d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
=====
UMM: b'33\x00\x00\x00\x0c\xf0n\x0b\x82\x08\xe7\x86\xdd`\x02\x81k\x02\x00\x11\x04\xfe\x80\x00\x00\x00\x00\x00\x00\xa8\xff1qU\xa6-\x1f\xff\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x07l\x07l\x02\x00\xd4\x0bNOTIFY * HTTP/1.1\r\nHost: [FF02::C]:1900\r\nNT: urn:schemas-upnp-org:service:AVTransport:1\r\nNTS: ssdp:alive\r\nLocation: http://[fe80::a8ff:3171:55a6:2d1f]:2869/upnphost/udhisapi.dll?content=uuid:2c0cee11-398d-4d6f-a585-7d5928f47c2f\r\nUSN: uuid:2c0cee11-398d-4d6f-a585-7d5928f47c2f::urn:schemas-upnp-org:service:AVTransport:1\r\nCache-Control: max-age=1800\r\nServer: Microsoft-Windows/10.0 UPnP/1.0 UPnP-Device-Host/1.0\r\nOPT:"http://schemas.upnp.org/upnp/1/0/"; ns=01\r\n01-NLS: 5f6e203ccbe9e2857fe3b8bc2913bf6c\r\n\r\n'
b'\x01\x00^\x7f\xff\xfa\xf0n\x0b\x82\x08\xe7\x08\x00E\x00\x02\x16\xf4\x84\x00\x00\x04\x11\x0f\xac\xc0\xa8\x00\x04\xef\xff\xff\xfa\x07l\x07l\x02\x02o\x10NOTIFY * HTTP/1.1\r\nHost: 239.255.255.250:1900\r\nNT: urn:schemas-upnp-org:service:ConnectionManager:1\r\nNTS: ssdp:alive\r\nLocation: http://192.168.0.4:2869/upnphost/udhisapi.dll?content=uuid:2c0cee11-398d-4d6f-a585-7d5928f47c2f\r\nUSN: uuid:2c0cee11-398d-4d6f-a585-7d5928f47c2f::urn:schemas-upnp-org:service:ConnectionManager:1\r\nCache-Control: max-age=1800\r\nServer: Microsoft-Windows/10.0 UPnP/1.0 UPnP-Device-Host/1.0\r\nOPT:"http://schemas.upnp.org/upnp/1/0/"; ns=01\r\n01-NLS: 5f6e203ccbe9e2857fe3b8bc2913bf6c\r\n\r\n'
"""
