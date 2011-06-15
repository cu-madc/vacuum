#!/bin/sh

# First set up the kernel to release the ports as soon as they are released.
sysctl -w net.ipv4.tcp_tw_reuse=1
sysctl -w net.ipv4.tcp_tw_recycle=1

# Second set up the alternate ip addresses for the existing network interfaces
ifconfig eth0:1 10.0.1.10 netmask 255.255.255.0
ifconfig eth0:2 10.0.1.11 netmask 255.255.255.0


