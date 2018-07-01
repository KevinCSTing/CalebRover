#!/usr/bin/python
 
#import libraries we need
import random
import time #time library
import RPi.GPIO as GPIO
from picamera import PiCamera #import camera so we can record videos/ take snapshots
import time
import sys

GPIO.setmode(GPIO.BOARD)
#declare GPIO pins to be used for the wheels
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

# for the sensor
PIN_TRIGGER = 29 
PIN_ECHO = 31 
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN) 

def distance():
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    print "waiting for sensor to settle"
    time.sleep(2)

    print "calculating distance"
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
       pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) ==1:
       pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration / 0.000148, 2)
    print "distance: ", distance,"in"
    move(distance)

def move(dist):
    if dist > 5:
        print "forward"
        GPIO.output(7,False)
        GPIO.output(11,True)
        GPIO.output(13,True)
        GPIO.output(15,False)
        time.sleep(5)
        GPIO.output(7,False)
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,False)
        GPIO.cleanup()
    else:
        print "gonna crash"
    

distance()
			