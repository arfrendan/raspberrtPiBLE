s = "0000000000000000"
try:
    f  = open('/proc/cpuinfo','r')
    for line in f:
        if line[0:6] == "Serial":
            s = line[10:26]
    f.close()
except:
    s = -1
print(s,end='')