#!/usr/bin/env python3


import sys
import socket


url_toggle = False
# any argument will make the script print url as well
if len(sys.argv) >= 2:
    url_toggle = True

site_ignore = [b'play.google.com', b'appsitemsuggest-pa.clients6.google.com']
site_need_url = [b'raw.githubusercontent.com', b'youtube.com', b'www.google.com', b'badger.c5games.com', b'www.kongregate.com']

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind(("127.0.0.1", 5080))

    while True:
        data, addr = sock.recvfrom(8192)
        dataList = data.split()

        if len(dataList) == 3:
            site_index = 1
        else:
            site_index = 0
               
               
               
        if dataList[site_index] not in site_ignore:
            if url_toggle or (dataList[site_index] in site_need_url):
                print(data.split())
            else:
                print(data.split()[:-1])

        # sock.sendto(b"hi from server", addr)
