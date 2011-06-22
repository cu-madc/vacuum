#!/bin/sh

# First set up the kernel to release the ports as soon as they are released.
sysctl -w net.ipv4.tcp_tw_reuse=1
sysctl -w net.ipv4.tcp_tw_recycle=1

# Second set up the alternate ip addresses for the existing network interfaces
ifconfig eth0:1 10.0.1.10 netmask 255.255.255.0
ifconfig eth0:2 10.0.1.11 netmask 255.255.255.0
ifconfig eth0:3 10.0.1.12 netmask 255.255.255.0
ifconfig eth0:4 10.0.1.13 netmask 255.255.255.0
ifconfig eth0:5 10.0.1.14 netmask 255.255.255.0
ifconfig eth0:6 10.0.1.15 netmask 255.255.255.0
ifconfig eth0:7 10.0.1.16 netmask 255.255.255.0
ifconfig eth0:8 10.0.1.17 netmask 255.255.255.0
ifconfig eth0:9 10.0.1.18 netmask 255.255.255.0
ifconfig eth0:10 10.0.1.19 netmask 255.255.255.0
ifconfig eth0:11 10.0.1.20 netmask 255.255.255.0
ifconfig eth0:12 10.0.1.21 netmask 255.255.255.0


