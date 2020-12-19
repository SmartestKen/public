#!/bin/bash

for pid in $(pidof -x "init.sh")
do
    if [ $pid != $$ ] 
    then
        kill $pid
    fi 
done


# prepare mitmdump for transparent proxying
sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv6.conf.all.forwarding=1
sysctl -w net.ipv4.conf.all.send_redirects=0

iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner root --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner root --dport 443 -j REDIRECT --to-port 8080
ip6tables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner root --dport 80 -j REDIRECT --to-port 8080
ip6tables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner root --dport 443 -j REDIRECT --to-port 8080

iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8080
ip6tables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
ip6tables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8080

# block vnc default port
iptables -A OUTPUT -p tcp -m owner ! --uid-owner root --dport 5900 -j DROP
ip6tables -A OUTPUT -p tcp -m owner ! --uid-owner root --dport 5900 -j DROP


# ensure only one instance
pkill mitmdump
# run mitmproxy on startup
mitmdump --mode transparent --set block_global=false --set stream_large_bodies=1 --set ssl_insecure=true --set stream_websockets=true -s /temp/mitmproxy_config.py -q & 


/temp/sync.sh



# release
signal=9999999999
while true
do
    internet_time=`wget -qSO- --max-redirect=0 google.com 2>&1`
    if [[ $? = 8 ]]
    then
        internet_time=`date +%s "$(grep Date: <<< "$internet_time" | cut -d' ' -f5-8)Z" >/dev/null`
    else
        continue
    fi
    
    # now we have the correct epoch
    
    # enable release
    if [[ $signal == "9999999999" && -f "/home/public/stop_init" ]]
    then
        signal=$((internet_time+86400))
    fi
    
    # retract release
    if [[ ! -f "/home/public/stop_init" ]]
    then
        signal=9999999999
    fi
        
    if [[ $internet_time -ge $signal ]]
    then
        echo "root:123" | chpasswd
    fi
    
    sleep 300
done
