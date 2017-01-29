#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys

TRIG = 11 #GPIO17
ECHO = 12 #GPIO18

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

def ultrasonicOnce():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)
    
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
    
    sys.stdout.flush()
    
    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()
    sys.stdout.flush()

    during = time2 - time1
    distance= during * 343.21 / 2 * 39.3701
    distance = round(distance, 2)
    retDis = '*' + str(distance) + '*'
    return retDis
    
def ultrasonicLoop():
    while True:
        dis = ultrasonicOnce()
        print dis
        sys.stdout.flush()
        time.sleep(.3)

def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
        setup()
        try:
            ultrasonicLoop()
        except KeyboardInterrupt:
            destroy()
