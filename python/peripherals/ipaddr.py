import socket
try:
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    print(ipaddr,end ='')
except:
    print(-1,end = '')