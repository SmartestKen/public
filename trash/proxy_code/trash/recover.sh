#!/bin/bash

iptables -X
ip6tables -X
iptables -t nat -X
ip6tables -t nat -X
iptables -t mangle -X
ip6tables -t mangle -X
iptables -F
ip6tables -F
iptables -t nat -F
ip6tables -t nat -F
iptables -t mangle -F
ip6tables -t mangle -F







