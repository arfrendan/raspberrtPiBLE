def get_temperature():
    file  = open("/sys/class/thermal/thermal_zone0/temp")
    temp = float(file.read())/1000
    file.close()
    return temp

if __name__ == "__main__":
    print(get_temperature(),end='')
