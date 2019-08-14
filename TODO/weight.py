import time
import RPi.GPIO as GPIO
import os
SCK_PIN = 23
SDA_PIN = 24
calibration = 0

def timeout():
    time.sleep(5)
    print('timeout')
    
def calibration_check():
    global calibration
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SCK_PIN,GPIO.OUT,initial = GPIO.LOW)
    GPIO.setup(SDA_PIN,GPIO.IN)
    GPIO.output(SCK_PIN,GPIO.LOW)
    while GPIO.input(SCK_PIN):
        pass
    data = 0
    while GPIO.input(SDA_PIN):
        pass
    time.sleep(0.001)
    
    for i in range(24):
        GPIO.output(SCK_PIN,GPIO.HIGH)
        while not GPIO.input(SCK_PIN):
            time.sleep(0.001)
        data = data*2
        GPIO.output(SCK_PIN,GPIO.LOW)
        while GPIO.input(SCK_PIN):
            pass
        if GPIO.input(SDA_PIN):
            data += 1
    GPIO.output(SCK_PIN,GPIO.HIGH)
    GPIO.output(SCK_PIN,GPIO.LOW)
    calibration = data
    calibration_file = open('/home/pi/test/python/peripherals/weight.txt','w')
    calibration_file.write(str(calibration))
    calibration_file.close()
    
def init():
    global calibration
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SCK_PIN,GPIO.OUT,initial = GPIO.LOW)
    GPIO.setup(SDA_PIN,GPIO.IN)
    GPIO.output(SCK_PIN,GPIO.LOW)
    calibration_file = open('/home/pi/test/python/peripherals/weight.txt','r')
    calibration = int(calibration_file.readline())
    calibration_file.close()
    
    
def check_weight():
    while GPIO.input(SCK_PIN):
        pass
    data = 0
    while GPIO.input(SDA_PIN):
        pass
    time.sleep(0.001)
    for i in range(24):
        GPIO.output(SCK_PIN,GPIO.HIGH)
        while not GPIO.input(SCK_PIN):
            time.sleep(0.001)
        data = data*2
        GPIO.output(SCK_PIN,GPIO.LOW)
        while GPIO.input(SCK_PIN):
            pass
        if GPIO.input(SDA_PIN):
            data += 1
            
    GPIO.output(SCK_PIN,GPIO.HIGH)
    GPIO.output(SCK_PIN,GPIO.LOW)
    data = (data - calibration+200)/415
    #print (data)
    return data
    
if __name__ == '__main__':
    """
    t = threading.Thread(target = timeout)
    t.setDaemon(True)
    t.start()
    
    t.join(2)
    print("over")
    """
    if os.path.exists('/home/pi/test/python/peripherals/weight.txt'):
        init()
    else:
        calibration_check()
    while True:
        print(check_weight())
        time.sleep(1)