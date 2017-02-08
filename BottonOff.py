#!/usr/bin/env python
import RPi.GPIO as GPIO
import os

BtnPin = 15 #GPIO22

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback=detect, bouncetime=200)

def detect(chn):
        print os.popen("sudo shutdown now")

def loop():
	while True:		
		pass

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()

