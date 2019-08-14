import time
import RPi.GPIO as GPIO




def checkdist():
    TRIG_PIN = 2
    ECHO_PIN = 3

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN,GPIO.OUT,initial = GPIO.LOW)
    GPIO.setup(ECHO_PIN,GPIO.IN)
    GPIO.output(TRIG_PIN,GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN,GPIO.LOW)
    t1 = time.time()
    while not GPIO.input(ECHO_PIN):
        pass
    while GPIO.input(ECHO_PIN):
        pass
    t2 = time.time()
    return(t2-t1)*34000/2


if __name__ == '__main__':
    try:
        min_distance = 1000.0
        for i in range(1,300):
            print('distance:'+str(checkdist()))
            if(checkdist()<min_distance):
                min_distance = checkdist()
            time.sleep(0.5)
        print('min_distance:' + str(min_distance))
    except KeyboardInterrupt:
        GPIO.cleanup()

