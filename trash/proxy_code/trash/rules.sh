#!/bin/bash




sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv6.conf.all.forwarding=1
sysctl -w net.ipv4.conf.all.send_redirects=0

# for testing, in real application, probably need to use new port for each upstream connection?
# or use the user match.

iptables -t nat -A OUTPUT -m tcp --sport ! 8080 --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -A OUTPUT -m tcp --sport ! 8080 --dport 443 -j REDIRECT --to-port 8080


ip6tables -t nat -A OUTPUT -m tcp --sport ! 8080 --dport 80 -j REDIRECT --to-port 8080
ip6tables -t nat -A OUTPUT -m tcp --sport ! 8080 --dport 443 -j REDIRECT --to-port 8080
    








