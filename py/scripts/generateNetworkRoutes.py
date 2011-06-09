#!/usr/bin/python
import sys
num_req_arguments = 8

# Usage information
if len(sys.argv) < num_req_arguments:
    print "Usage:"
    print "   ",sys.argv[0],"interface1","interface1ip","interface2","interface2ip","fakeip","netmask","gatewayip"
    exit(1)

import os

interface1 = sys.argv[1]
interface1ip = sys.argv[2]
interface2 = sys.argv[3]
interface2ip = sys.argv[4]
fakeip = sys.argv[5]
netmask = sys.argv[6]
gatewayip = sys.argv[7]

print "ifconfig", interface1, interface1ip, "netmask", netmask
print "ifconfig", interface2, interface2ip, "netmask", netmask
print "iptables","-t","nat","-A","PREROUTING","-d",fakeip,"-i",interface2,"-j","DNAT","--to-destination",interface2ip
#print "iptables","-t","nat","-A","POSTROUTING","-s",interface2ip,"-d",interface1ip + "/24","-j","SNAT","--to-source",fakeip
#print "route","add",fakeip,"via",interface1,"gw",gatewayip

if sys.argv[8] == '-p':
    exit(0)

os.execl("/sbin/ifconfig", interface1, interface1ip, "netmask", netmask)
os.execl("/sbin/ifconfig", interface2, interface2ip, "netmask", netmask)

os.execl("/sbin/iptables","-t","nat","-A","PREROUTING","-d",fakeip,"-i",
         interface2,"-j","DNAT","--to-destination",interface2ip)

#os.execl("/sbin/iptables","-t","nat","-A","POSTROUTING","-s",interface2ip,"-d",
#         interface1ip + "/24","-j","SNAT","--to-source",fakeip)

#os.execl("/sbin/route","add",fakeip,"via",interface1,"gw",gatewayip)

