from mitmproxy import http
import socket


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 5080))
except Exception as e:
    pass




def request(flow: http.HTTPFlow):
    global sock

    host = flow.request.pretty_host
    tokens = host.split(".")
    prefix = "pass "


    for item in blacklist.get(sum(bytearray(tokens[-2] + tokens[-1], "utf8"))):
        if host.endswith('.' + item[1:]) or host == item:
            flow.response = http.HTTPResponse.make(501)
            prefix = "block "


    try:
        sock.send((prefix + host).encode())
    except Exception as e:
        pass



try:
    with open('/temp/blacklist.txt', 'r') as f:
        content = f.readlines()
    blacklist = dict()
    for item in content:
        item = item.strip()
        tokens = item.split(".")
        if len(tokens) >= 2:
            hash = sum(bytearray(tokens[-2] + tokens[-1], "utf8"))
            if blacklist.get(hash) == None:
                blacklist[hash] = []
            blacklist[hash].append(item)
except Exception as e:
    print("failure in readSites")
    blacklist = []
