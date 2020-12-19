import socket  # for socket
import time



# default port for socket
port = 80
# host_ip = '::1'
host_ip = '132.239.145.52'
count = 0

while True:
    # connecting to the server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host_ip, port))
        msg = "I am a client" + str(count)

        s.send(msg.encode('utf-8'))

        print("I connect", msg)
        count += 1
        s.close()
    except:
        print("no one detected")
    time.sleep(5)
